#!/usr/bin/env bash
#
# PostgreSQL Rollback Script
#
# Safely removes PostgreSQL deployment with:
# - Optional data backup before removal
# - PVC deletion (optional)
# - Clean state verification
#
# Usage:
#   bash rollback.sh               # Remove deployment, keep PVC
#   bash rollback.sh --delete-pvc  # Remove deployment and data
#   bash rollback.sh --no-backup   # Skip backup before removal
#
# Exit Codes:
#   0 - Success
#   1 - Failure

set -euo pipefail

# Configuration
NAMESPACE="${NAMESPACE:-postgres}"
RELEASE_NAME="${RELEASE_NAME:-postgres}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/.postgres-deploy.log"

# Options
DELETE_PVC=false
SKIP_BACKUP=false
FORCE=false

# Colors (disabled if not terminal)
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
            --delete-pvc)
                DELETE_PVC=true
                shift
                ;;
            --no-backup)
                SKIP_BACKUP=true
                shift
                ;;
            --force|-f)
                FORCE=true
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --delete-pvc    Delete PersistentVolumeClaim (removes all data)"
                echo "  --no-backup     Skip backup before removal"
                echo "  --force, -f     Skip confirmation prompts"
                echo "  -h, --help      Show this help"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
}

# Check if deployment exists
check_deployment_exists() {
    if helm status "$RELEASE_NAME" -n "$NAMESPACE" &>/dev/null; then
        return 0
    else
        return 1
    fi
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

# Create backup before removal
create_backup() {
    log_info "Creating backup before removal..."

    if [[ -f "${SCRIPT_DIR}/backup.py" ]]; then
        if python3 "${SCRIPT_DIR}/backup.py" --verbose; then
            log_info "Backup created successfully"
            return 0
        else
            log_warn "Backup failed"
            return 1
        fi
    else
        log_warn "Backup script not found, skipping backup"
        return 0
    fi
}

# Remove Helm release
remove_helm_release() {
    log_info "Removing Helm release '$RELEASE_NAME'..."

    if helm uninstall "$RELEASE_NAME" -n "$NAMESPACE" --wait; then
        log_info "Helm release removed"
        return 0
    else
        log_error "Failed to remove Helm release"
        return 1
    fi
}

# Delete PVC
delete_pvc() {
    log_info "Deleting PersistentVolumeClaims..."

    # Get PVCs for the release
    local pvcs
    pvcs=$(kubectl get pvc -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" -o name 2>/dev/null || echo "")

    if [[ -z "$pvcs" ]]; then
        log_info "No PVCs found to delete"
        return 0
    fi

    echo "$pvcs" | while read -r pvc; do
        if [[ -n "$pvc" ]]; then
            log_info "Deleting $pvc..."
            kubectl delete "$pvc" -n "$NAMESPACE" --wait=true
        fi
    done

    log_info "PVCs deleted"
    return 0
}

# Delete namespace if empty
cleanup_namespace() {
    log_info "Checking namespace '$NAMESPACE'..."

    # Count resources in namespace
    local resource_count
    resource_count=$(kubectl get all -n "$NAMESPACE" --no-headers 2>/dev/null | wc -l)

    if [[ "$resource_count" -eq 0 ]]; then
        if confirm "Namespace '$NAMESPACE' is empty. Delete it?"; then
            kubectl delete namespace "$NAMESPACE" --wait=true
            log_info "Namespace '$NAMESPACE' deleted"
        fi
    else
        log_info "Namespace '$NAMESPACE' still has $resource_count resource(s), keeping it"
    fi
}

# Verify clean state
verify_clean_state() {
    log_info "Verifying clean state..."

    local issues=0

    # Check for remaining pods
    local pods
    pods=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --no-headers 2>/dev/null | wc -l)
    if [[ "$pods" -gt 0 ]]; then
        log_warn "$pods pod(s) still exist"
        ((issues++))
    fi

    # Check for remaining services
    local services
    services=$(kubectl get svc -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --no-headers 2>/dev/null | wc -l)
    if [[ "$services" -gt 0 ]]; then
        log_warn "$services service(s) still exist"
        ((issues++))
    fi

    # Check for remaining secrets
    local secrets
    secrets=$(kubectl get secrets -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --no-headers 2>/dev/null | wc -l)
    if [[ "$secrets" -gt 0 ]]; then
        log_warn "$secrets secret(s) still exist"
        ((issues++))
    fi

    # Check PVCs if we requested deletion
    if [[ "$DELETE_PVC" == "true" ]]; then
        local pvcs
        pvcs=$(kubectl get pvc -n "$NAMESPACE" -l "app.kubernetes.io/instance=$RELEASE_NAME" --no-headers 2>/dev/null | wc -l)
        if [[ "$pvcs" -gt 0 ]]; then
            log_warn "$pvcs PVC(s) still exist"
            ((issues++))
        fi
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

    echo "=== PostgreSQL Rollback Started $(date -u +"%Y-%m-%dT%H:%M:%SZ") ===" >> "$LOG_FILE"

    log_info "Starting PostgreSQL rollback"
    log_info "Namespace: $NAMESPACE"
    log_info "Release: $RELEASE_NAME"
    log_info "Delete PVC: $DELETE_PVC"

    # Check if deployment exists
    if ! check_deployment_exists; then
        log_info "No deployment found for '$RELEASE_NAME' in namespace '$NAMESPACE'"
        echo "[OK] Nothing to rollback"
        exit 0
    fi

    # Confirmation
    if [[ "$DELETE_PVC" == "true" ]]; then
        if ! confirm "This will DELETE ALL DATA. Are you sure?"; then
            log_info "Rollback cancelled by user"
            echo "[CANCELLED] Rollback cancelled"
            exit 0
        fi
    fi

    # Create backup (unless skipped)
    if [[ "$SKIP_BACKUP" != "true" ]]; then
        if ! create_backup; then
            if ! confirm "Backup failed. Continue anyway?"; then
                log_info "Rollback cancelled due to backup failure"
                echo "[CANCELLED] Backup failed, rollback cancelled"
                exit 1
            fi
        fi
    fi

    # Remove Helm release
    if ! remove_helm_release; then
        log_error "Failed to remove Helm release"
        echo "[ERROR] Rollback failed"
        exit 1
    fi

    # Delete PVC if requested
    if [[ "$DELETE_PVC" == "true" ]]; then
        if ! delete_pvc; then
            log_warn "PVC deletion had issues"
        fi
    fi

    # Optional: cleanup empty namespace
    cleanup_namespace

    # Verify clean state
    if verify_clean_state; then
        log_info "Rollback completed successfully"
        echo "[OK] PostgreSQL removed"
    else
        log_warn "Rollback completed with warnings"
        echo "[OK] PostgreSQL removed (with warnings)"
    fi

    # Clean up connection file
    rm -f "${SCRIPT_DIR}/.connection"

    exit 0
}

main "$@"
