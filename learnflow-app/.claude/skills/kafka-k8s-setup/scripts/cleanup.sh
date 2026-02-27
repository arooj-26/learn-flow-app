#!/usr/bin/env bash
#
# Kafka Cleanup Script
#
# Removes Kafka deployment from Kubernetes:
# - Uninstalls Helm release
# - Deletes Zookeeper
# - Optionally deletes namespace
# - Verifies clean state
#
# Usage:
#   bash cleanup.sh
#   bash cleanup.sh --force
#   bash cleanup.sh --delete-namespace
#
# Exit Codes:
#   0 - Success
#   1 - Failure

set -euo pipefail

# Configuration
NAMESPACE="${NAMESPACE:-kafka}"
RELEASE_NAME="${RELEASE_NAME:-kafka}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/.kafka-deploy.log"

# Options
FORCE=false
DELETE_NAMESPACE=false

# Colors
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    NC=''
fi

# Logging
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"

    case "$level" in
        ERROR) echo -e "${RED}[$level]${NC} $message" >&2 ;;
        WARN)  echo -e "${YELLOW}[$level]${NC} $message" >&2 ;;
        INFO)  echo -e "${GREEN}[$level]${NC} $message" ;;
    esac
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force|-f)
                FORCE=true
                shift
                ;;
            --delete-namespace)
                DELETE_NAMESPACE=true
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --force, -f          Skip confirmation prompts"
                echo "  --delete-namespace   Delete the namespace after cleanup"
                echo "  -h, --help           Show this help"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
}

# Confirm action
confirm() {
    local message="$1"

    if [[ "$FORCE" == "true" ]]; then
        return 0
    fi

    echo -e "${YELLOW}$message${NC}"
    read -p "Continue? [y/N] " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# Check if deployment exists
check_deployment_exists() {
    if helm status "$RELEASE_NAME" -n "$NAMESPACE" &>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Uninstall Helm release
uninstall_kafka() {
    log_info "Uninstalling Kafka Helm release..."

    if helm uninstall "$RELEASE_NAME" -n "$NAMESPACE" --wait 2>/dev/null; then
        log_info "Kafka Helm release uninstalled"
        return 0
    else
        log_warn "Helm uninstall returned error (may already be deleted)"
        return 0
    fi
}

# Delete remaining resources
delete_remaining_resources() {
    log_info "Cleaning up remaining resources..."

    # Delete any remaining pods
    kubectl delete pods -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --ignore-not-found=true 2>/dev/null || true

    # Delete any remaining services
    kubectl delete svc -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --ignore-not-found=true 2>/dev/null || true

    # Delete any remaining PVCs
    kubectl delete pvc -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --ignore-not-found=true 2>/dev/null || true

    # Delete any remaining secrets
    kubectl delete secrets -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --ignore-not-found=true 2>/dev/null || true

    # Delete any remaining configmaps
    kubectl delete configmaps -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --ignore-not-found=true 2>/dev/null || true

    log_info "Remaining resources cleaned up"
}

# Delete namespace
delete_namespace() {
    if [[ "$DELETE_NAMESPACE" != "true" ]]; then
        return 0
    fi

    log_info "Deleting namespace '$NAMESPACE'..."

    # Check if namespace is empty
    local resource_count
    resource_count=$(kubectl get all -n "$NAMESPACE" --no-headers 2>/dev/null | wc -l)

    if [[ "$resource_count" -gt 0 ]]; then
        log_warn "Namespace still has $resource_count resource(s)"
        if ! confirm "Delete namespace anyway?"; then
            log_info "Skipping namespace deletion"
            return 0
        fi
    fi

    if kubectl delete namespace "$NAMESPACE" --wait=true 2>/dev/null; then
        log_info "Namespace '$NAMESPACE' deleted"
    else
        log_warn "Failed to delete namespace (may not exist)"
    fi
}

# Verify clean state
verify_clean() {
    log_info "Verifying clean state..."

    local issues=0

    # Check namespace exists
    if ! kubectl get namespace "$NAMESPACE" &>/dev/null; then
        log_info "Namespace '$NAMESPACE' does not exist (clean)"
        return 0
    fi

    # Check for remaining pods
    local pods
    pods=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --no-headers 2>/dev/null | wc -l)
    if [[ "$pods" -gt 0 ]]; then
        log_warn "$pods pod(s) still exist"
        ((issues++))
    fi

    # Check for remaining PVCs
    local pvcs
    pvcs=$(kubectl get pvc -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --no-headers 2>/dev/null | wc -l)
    if [[ "$pvcs" -gt 0 ]]; then
        log_warn "$pvcs PVC(s) still exist"
        ((issues++))
    fi

    if [[ "$issues" -eq 0 ]]; then
        log_info "Clean state verified"
        return 0
    else
        log_warn "$issues issue(s) found during verification"
        return 1
    fi
}

# Main
main() {
    parse_args "$@"

    echo "=== Kafka Cleanup Started $(date -u +"%Y-%m-%dT%H:%M:%SZ") ===" >> "$LOG_FILE"

    log_info "Starting Kafka cleanup"
    log_info "Namespace: $NAMESPACE"
    log_info "Release: $RELEASE_NAME"

    # Check if deployment exists
    if ! check_deployment_exists; then
        log_info "No Kafka deployment found"
        echo "[OK] Nothing to clean up"
        exit 0
    fi

    # Confirmation
    if ! confirm "This will remove Kafka from namespace '$NAMESPACE'. Continue?"; then
        log_info "Cleanup cancelled by user"
        echo "[CANCELLED] Cleanup cancelled"
        exit 0
    fi

    # Uninstall Kafka
    if ! uninstall_kafka; then
        log_error "Failed to uninstall Kafka"
        echo "[ERROR] Cleanup failed"
        exit 1
    fi

    # Delete remaining resources
    delete_remaining_resources

    # Optionally delete namespace
    delete_namespace

    # Verify clean state
    if verify_clean; then
        log_info "Kafka cleanup completed successfully"
        echo "[OK] Kafka removed"
    else
        log_warn "Kafka cleanup completed with warnings"
        echo "[OK] Kafka removed (with warnings)"
    fi

    # Clean up connection file
    rm -f "${SCRIPT_DIR}/.connection"

    exit 0
}

main "$@"
