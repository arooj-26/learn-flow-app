#!/usr/bin/env bash
# cleanup.sh - Remove Docusaurus deployment artifacts and rollback deployments.
#
# Supports target-specific cleanup for GitHub Pages, Vercel, Netlify, and K8s.
# Includes confirmation prompt (--force to skip), --keep-content to only remove
# deployment artifacts, and --delete-namespace for K8s.
#
# Exit codes:
#   0 - Success
#   1 - Fatal error
#   2 - Prerequisites not met
#   3 - Cleanup failed
#   4 - User cancelled

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEPLOY_TARGET="${DEPLOY_TARGET:-github-pages}"
PROJECT_DIR="${PROJECT_DIR:-.}"
NAMESPACE="${NAMESPACE:-docs}"
IMAGE_NAME="${IMAGE_NAME:-docs-site}"
FORCE="${FORCE:-0}"
KEEP_CONTENT="${KEEP_CONTENT:-0}"
DELETE_NAMESPACE="${DELETE_NAMESPACE:-0}"
LOG_FILE="${LOG_FILE:-.docusaurus-deploy.log}"
VERBOSE="${VERBOSE:-0}"

# Vercel
VERCEL_TOKEN="${VERCEL_TOKEN:-}"
VERCEL_PROJECT_ID="${VERCEL_PROJECT_ID:-}"

# Netlify
NETLIFY_TOKEN="${NETLIFY_TOKEN:-}"
NETLIFY_SITE_ID="${NETLIFY_SITE_ID:-}"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
log() {
    local level="$1"; shift
    local msg="$*"
    local ts
    ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")"
    echo "[$ts] [$level] $msg" >> "$LOG_FILE"
    if [[ "$VERBOSE" == "1" ]] || [[ "$level" == "ERROR" ]]; then
        echo "[$level] $msg" >&2
    fi
}

cleanup_trap() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]] && [[ $exit_code -ne 4 ]]; then
        log "ERROR" "cleanup.sh failed with exit code $exit_code"
    fi
}
trap cleanup_trap EXIT

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --force)
                FORCE=1
                shift
                ;;
            --keep-content)
                KEEP_CONTENT=1
                shift
                ;;
            --delete-namespace)
                DELETE_NAMESPACE=1
                shift
                ;;
            --target)
                DEPLOY_TARGET="$2"
                shift 2
                ;;
            --project-dir)
                PROJECT_DIR="$2"
                shift 2
                ;;
            --namespace)
                NAMESPACE="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=1
                shift
                ;;
            *)
                log "WARN" "Unknown argument: $1"
                shift
                ;;
        esac
    done
}

# ---------------------------------------------------------------------------
# Confirmation prompt
# ---------------------------------------------------------------------------
confirm_cleanup() {
    if [[ "$FORCE" == "1" ]]; then
        return 0
    fi

    echo "This will remove deployment artifacts for target: $DEPLOY_TARGET"
    if [[ "$KEEP_CONTENT" == "0" ]]; then
        echo "WARNING: This will also remove build output and configuration files."
    else
        echo "Content will be preserved (--keep-content)."
    fi

    read -r -p "Continue? [y/N] " response
    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        *)
            log "INFO" "Cleanup cancelled by user"
            exit 4
            ;;
    esac
}

# ---------------------------------------------------------------------------
# GitHub Pages cleanup
# ---------------------------------------------------------------------------
cleanup_github_pages() {
    log "INFO" "Cleaning up GitHub Pages deployment..."

    # Remove build artifacts
    if [[ "$KEEP_CONTENT" == "0" ]]; then
        rm -rf "$PROJECT_DIR/build"
        rm -rf "$PROJECT_DIR/.docusaurus"
        log "INFO" "Removed build/ and .docusaurus/"
    fi

    # Remove gh-pages branch (local only)
    if command -v git &>/dev/null; then
        if git -C "$PROJECT_DIR" branch --list gh-pages | grep -q "gh-pages"; then
            git -C "$PROJECT_DIR" branch -D gh-pages >> "$LOG_FILE" 2>&1 || true
            log "INFO" "Removed local gh-pages branch"
        fi
    fi

    # Remove CI/CD workflow
    local workflow="$PROJECT_DIR/.github/workflows/deploy-docs.yml"
    if [[ -f "$workflow" ]]; then
        rm -f "$workflow"
        log "INFO" "Removed deploy-docs.yml workflow"
    fi

    log "INFO" "GitHub Pages cleanup complete"
}

# ---------------------------------------------------------------------------
# Vercel cleanup
# ---------------------------------------------------------------------------
cleanup_vercel() {
    log "INFO" "Cleaning up Vercel deployment..."

    local vercel_cmd="vercel"
    if ! command -v vercel &>/dev/null; then
        if command -v npx &>/dev/null; then
            vercel_cmd="npx vercel"
        else
            log "WARN" "vercel CLI not available – skipping remote cleanup"
        fi
    fi

    # Remove Vercel project
    if command -v vercel &>/dev/null || command -v npx &>/dev/null; then
        local token_flag=""
        if [[ -n "$VERCEL_TOKEN" ]]; then
            token_flag="--token $VERCEL_TOKEN"
        fi

        (cd "$PROJECT_DIR" && $vercel_cmd remove --yes $token_flag) >> "$LOG_FILE" 2>&1 || {
            log "WARN" "Vercel project removal failed (may need manual cleanup)"
        }
    fi

    # Remove config files
    if [[ "$KEEP_CONTENT" == "0" ]]; then
        rm -f "$PROJECT_DIR/vercel.json"
        rm -f "$PROJECT_DIR/.vercel/project.json"
        rmdir "$PROJECT_DIR/.vercel" 2>/dev/null || true
        rm -rf "$PROJECT_DIR/build"
        log "INFO" "Removed Vercel config and build artifacts"
    fi

    log "INFO" "Vercel cleanup complete"
}

# ---------------------------------------------------------------------------
# Netlify cleanup
# ---------------------------------------------------------------------------
cleanup_netlify() {
    log "INFO" "Cleaning up Netlify deployment..."

    local netlify_cmd="netlify"
    if ! command -v netlify &>/dev/null; then
        if command -v npx &>/dev/null; then
            netlify_cmd="npx netlify-cli"
        else
            log "WARN" "netlify CLI not available – skipping remote cleanup"
        fi
    fi

    # Delete Netlify site
    if [[ -n "$NETLIFY_SITE_ID" ]]; then
        local token_flag=""
        if [[ -n "$NETLIFY_TOKEN" ]]; then
            token_flag="--auth $NETLIFY_TOKEN"
        fi

        ($netlify_cmd sites:delete "$NETLIFY_SITE_ID" --force $token_flag) >> "$LOG_FILE" 2>&1 || {
            log "WARN" "Netlify site deletion failed (may need manual cleanup)"
        }
    fi

    # Remove config files
    if [[ "$KEEP_CONTENT" == "0" ]]; then
        rm -f "$PROJECT_DIR/netlify.toml"
        rm -rf "$PROJECT_DIR/build"
        log "INFO" "Removed Netlify config and build artifacts"
    fi

    log "INFO" "Netlify cleanup complete"
}

# ---------------------------------------------------------------------------
# Kubernetes cleanup
# ---------------------------------------------------------------------------
cleanup_k8s() {
    log "INFO" "Cleaning up Kubernetes deployment..."

    if ! command -v kubectl &>/dev/null; then
        log "ERROR" "kubectl is required for K8s cleanup"
        exit 2
    fi

    # Delete K8s resources
    local k8s_dir="$PROJECT_DIR/k8s"
    if [[ -d "$k8s_dir" ]]; then
        kubectl delete -f "$k8s_dir/" --ignore-not-found >> "$LOG_FILE" 2>&1 || {
            log "WARN" "Some K8s resources could not be deleted"
        }
        log "INFO" "Deleted K8s resources from manifests"
    else
        # Delete by label
        kubectl delete deployment "$IMAGE_NAME" -n "$NAMESPACE" --ignore-not-found >> "$LOG_FILE" 2>&1
        kubectl delete service "$IMAGE_NAME" -n "$NAMESPACE" --ignore-not-found >> "$LOG_FILE" 2>&1
        kubectl delete configmap "${IMAGE_NAME}-config" -n "$NAMESPACE" --ignore-not-found >> "$LOG_FILE" 2>&1
        log "INFO" "Deleted K8s resources by name"
    fi

    # Delete namespace if requested
    if [[ "$DELETE_NAMESPACE" == "1" ]]; then
        kubectl delete namespace "$NAMESPACE" --ignore-not-found >> "$LOG_FILE" 2>&1 || {
            log "WARN" "Namespace deletion failed"
        }
        log "INFO" "Deleted namespace: $NAMESPACE"
    fi

    # Remove local Docker image
    if command -v docker &>/dev/null; then
        docker rmi "${IMAGE_NAME}:latest" >> "$LOG_FILE" 2>&1 || true
        log "INFO" "Removed local Docker image"
    fi

    # Remove artifacts
    if [[ "$KEEP_CONTENT" == "0" ]]; then
        rm -rf "$PROJECT_DIR/k8s"
        rm -f "$PROJECT_DIR/Dockerfile"
        rm -rf "$PROJECT_DIR/build"
        log "INFO" "Removed K8s manifests, Dockerfile, and build artifacts"
    fi

    log "INFO" "Kubernetes cleanup complete"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    parse_args "$@"

    log "INFO" "=== Cleanup started ==="
    log "INFO" "Target: $DEPLOY_TARGET | Project: $PROJECT_DIR | Force: $FORCE | Keep content: $KEEP_CONTENT"

    confirm_cleanup

    case "$DEPLOY_TARGET" in
        github-pages)
            cleanup_github_pages
            ;;
        vercel)
            cleanup_vercel
            ;;
        netlify)
            cleanup_netlify
            ;;
        k8s|kubernetes)
            cleanup_k8s
            ;;
        *)
            log "ERROR" "Unknown deploy target: $DEPLOY_TARGET"
            exit 3
            ;;
    esac

    log "INFO" "=== Cleanup complete ==="
    echo "[OK] Cleanup complete (target: ${DEPLOY_TARGET})"
}

main "$@"
