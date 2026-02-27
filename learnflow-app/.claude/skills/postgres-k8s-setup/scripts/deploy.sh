#!/usr/bin/env bash
#
# PostgreSQL Kubernetes Deployment Script
#
# Deploys PostgreSQL to Kubernetes using Bitnami Helm chart with:
# - Prerequisites validation
# - Idempotent deployment (safe to run multiple times)
# - Retry logic with backoff
# - Comprehensive logging
#
# Usage:
#   bash deploy.sh
#   NAMESPACE=myapp bash deploy.sh
#   DEBUG=1 bash deploy.sh
#
# Exit Codes:
#   0 - Success
#   1 - Fatal error
#   2 - Prerequisites not met (retryable)

set -euo pipefail

# Configuration
NAMESPACE="${NAMESPACE:-postgres}"
RELEASE_NAME="${RELEASE_NAME:-postgres}"
CHART_VERSION="${CHART_VERSION:-12.12.10}"
DATABASE_NAME="${DATABASE_NAME:-learnflow}"
HELM_TIMEOUT="${HELM_TIMEOUT:-5m}"
POD_WAIT_TIMEOUT="${POD_WAIT_TIMEOUT:-300}"  # 5 minutes
POD_CHECK_INTERVAL="${POD_CHECK_INTERVAL:-10}"  # seconds
MAX_RETRIES="${MAX_RETRIES:-3}"
RETRY_BACKOFF="${RETRY_BACKOFF:-30}"  # seconds

# Logging
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/.postgres-deploy.log"
DEBUG="${DEBUG:-0}"

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

# Logging functions
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"

    if [[ "$DEBUG" == "1" ]] || [[ "$level" == "ERROR" ]] || [[ "$level" == "INFO" ]]; then
        case "$level" in
            ERROR) echo -e "${RED}[$level]${NC} $message" >&2 ;;
            WARN)  echo -e "${YELLOW}[$level]${NC} $message" >&2 ;;
            INFO)  echo -e "${GREEN}[$level]${NC} $message" ;;
            DEBUG) echo "[$level] $message" ;;
        esac
    fi
}

log_debug() { log "DEBUG" "$@"; }
log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }

# Initialize log file
init_log() {
    echo "=== PostgreSQL Deployment Started $(date -u +"%Y-%m-%dT%H:%M:%SZ") ===" >> "$LOG_FILE"
}

# Cleanup function
cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        log_error "Deployment failed with exit code $exit_code"
        echo "[ERROR] Deployment failed. Check $LOG_FILE for details."
    fi
}
trap cleanup EXIT

# =============================================================================
# PREREQUISITES VALIDATION
# =============================================================================

validate_prerequisites() {
    log_info "Validating prerequisites..."
    local errors=0

    # Check kubectl
    if ! command -v kubectl &>/dev/null; then
        log_error "kubectl not found in PATH"
        echo "[ERROR] kubectl not found"
        ((errors++))
    else
        log_debug "kubectl found: $(command -v kubectl)"
    fi

    # Check helm
    if ! command -v helm &>/dev/null; then
        log_error "helm not found in PATH"
        echo "[ERROR] helm not found"
        ((errors++))
    else
        local helm_version
        helm_version=$(helm version --short 2>/dev/null | grep -oE 'v[0-9]+\.[0-9]+' | head -1)
        log_debug "helm version: $helm_version"

        # Check helm version >= 3.9
        local major minor
        major=$(echo "$helm_version" | cut -d. -f1 | tr -d 'v')
        minor=$(echo "$helm_version" | cut -d. -f2)
        if [[ "$major" -lt 3 ]] || { [[ "$major" -eq 3 ]] && [[ "$minor" -lt 9 ]]; }; then
            log_error "helm version $helm_version < 3.9 required"
            echo "[ERROR] helm 3.9+ required (found $helm_version)"
            ((errors++))
        fi
    fi

    # Check psql (optional but recommended)
    if ! command -v psql &>/dev/null; then
        log_warn "psql not found - verification will be limited"
    else
        log_debug "psql found: $(command -v psql)"
    fi

    # Check Kubernetes cluster accessibility
    if ! kubectl cluster-info &>/dev/null; then
        log_error "Kubernetes cluster not accessible"
        echo "[ERROR] Kubernetes not accessible"
        ((errors++))
    else
        local context
        context=$(kubectl config current-context 2>/dev/null || echo "unknown")
        log_debug "Kubernetes context: $context"
    fi

    # Check cluster resources (optional)
    if kubectl top nodes &>/dev/null; then
        local available_memory
        available_memory=$(kubectl top nodes --no-headers 2>/dev/null | awk '{sum += $4} END {print sum}' | tr -d 'Mi')
        log_debug "Cluster memory usage reported"
    fi

    if [[ $errors -gt 0 ]]; then
        log_error "Prerequisites validation failed with $errors error(s)"
        return 2
    fi

    log_info "Prerequisites validated successfully"
    return 0
}

# =============================================================================
# NAMESPACE MANAGEMENT
# =============================================================================

ensure_namespace() {
    log_info "Ensuring namespace '$NAMESPACE' exists..."

    if kubectl get namespace "$NAMESPACE" &>/dev/null; then
        log_debug "Namespace '$NAMESPACE' already exists"
    else
        log_info "Creating namespace '$NAMESPACE'..."
        if ! kubectl create namespace "$NAMESPACE"; then
            log_error "Failed to create namespace '$NAMESPACE'"
            return 1
        fi
        log_info "Namespace '$NAMESPACE' created"
    fi

    return 0
}

# =============================================================================
# HELM REPOSITORY
# =============================================================================

setup_helm_repo() {
    log_info "Setting up Bitnami Helm repository..."

    # Add repo (idempotent)
    if ! helm repo add bitnami https://charts.bitnami.com/bitnami 2>/dev/null; then
        log_debug "Bitnami repo may already exist, updating..."
    fi

    # Update repo
    log_debug "Updating Helm repositories..."
    if ! helm repo update &>/dev/null; then
        log_warn "Helm repo update failed, continuing with cached charts"
    fi

    log_info "Helm repository ready"
    return 0
}

# =============================================================================
# HELM DEPLOYMENT
# =============================================================================

deploy_postgresql() {
    log_info "Deploying PostgreSQL..."

    local attempt=1
    local deployed=false

    while [[ $attempt -le $MAX_RETRIES ]]; do
        log_info "Deployment attempt $attempt of $MAX_RETRIES..."

        # Check if release already exists
        local release_status
        release_status=$(helm status "$RELEASE_NAME" -n "$NAMESPACE" 2>/dev/null | grep -i status | head -1 || echo "")

        if [[ "$release_status" == *"deployed"* ]]; then
            log_info "Release '$RELEASE_NAME' already deployed, upgrading..."
            local cmd="upgrade"
        else
            log_info "Installing new release '$RELEASE_NAME'..."
            local cmd="install"
        fi

        # Build helm command
        local helm_cmd=(
            helm "$cmd" "$RELEASE_NAME" bitnami/postgresql
            --namespace "$NAMESPACE"
            --version "$CHART_VERSION"
            --set "auth.database=$DATABASE_NAME"
            --set "primary.persistence.enabled=true"
            --set "primary.persistence.size=8Gi"
            --wait
            --timeout "$HELM_TIMEOUT"
        )

        if [[ "$cmd" == "install" ]]; then
            helm_cmd+=(--create-namespace)
        fi

        log_debug "Executing: ${helm_cmd[*]}"

        if "${helm_cmd[@]}" >> "$LOG_FILE" 2>&1; then
            deployed=true
            break
        else
            log_warn "Deployment attempt $attempt failed"

            if [[ $attempt -lt $MAX_RETRIES ]]; then
                log_info "Waiting ${RETRY_BACKOFF}s before retry..."
                sleep "$RETRY_BACKOFF"
            fi
        fi

        ((attempt++))
    done

    if [[ "$deployed" != "true" ]]; then
        log_error "Deployment failed after $MAX_RETRIES attempts"
        return 1
    fi

    log_info "Helm deployment successful"
    return 0
}

# =============================================================================
# WAIT FOR POD
# =============================================================================

wait_for_pod() {
    log_info "Waiting for PostgreSQL pod to be ready..."

    local elapsed=0
    local pod_ready=false

    while [[ $elapsed -lt $POD_WAIT_TIMEOUT ]]; do
        local running_pods
        running_pods=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/name=postgresql" \
            --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)

        if [[ "$running_pods" -ge 1 ]]; then
            # Check if pod is actually ready (all containers)
            local ready_pods
            ready_pods=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/name=postgresql" \
                -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}' 2>/dev/null)

            if [[ "$ready_pods" == *"True"* ]]; then
                pod_ready=true
                break
            fi
        fi

        log_debug "Waiting for pod... ($elapsed/${POD_WAIT_TIMEOUT}s)"
        sleep "$POD_CHECK_INTERVAL"
        ((elapsed += POD_CHECK_INTERVAL))
    done

    if [[ "$pod_ready" != "true" ]]; then
        log_error "Pod failed to become ready within ${POD_WAIT_TIMEOUT}s"

        # Log pod status for debugging
        kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/name=postgresql" >> "$LOG_FILE" 2>&1
        kubectl describe pods -n "$NAMESPACE" -l "app.kubernetes.io/name=postgresql" >> "$LOG_FILE" 2>&1

        return 1
    fi

    log_info "PostgreSQL pod is ready"
    return 0
}

# =============================================================================
# CONNECTION DETAILS
# =============================================================================

get_connection_details() {
    log_info "Extracting connection details..."

    # Get service hostname
    local host
    host="${RELEASE_NAME}-postgresql.${NAMESPACE}.svc.cluster.local"

    # Get port (default 5432)
    local port=5432

    # Get password from secret
    local password
    password=$(kubectl get secret "${RELEASE_NAME}-postgresql" -n "$NAMESPACE" \
        -o jsonpath='{.data.postgres-password}' 2>/dev/null | base64 -d)

    if [[ -z "$password" ]]; then
        log_warn "Could not retrieve password from secret"
    fi

    log_debug "Host: $host"
    log_debug "Port: $port"
    log_debug "Database: $DATABASE_NAME"

    # Store connection info
    echo "POSTGRES_HOST=$host" > "${SCRIPT_DIR}/.connection"
    echo "POSTGRES_PORT=$port" >> "${SCRIPT_DIR}/.connection"
    echo "POSTGRES_USER=postgres" >> "${SCRIPT_DIR}/.connection"
    echo "POSTGRES_DB=$DATABASE_NAME" >> "${SCRIPT_DIR}/.connection"

    log_info "Connection details saved to ${SCRIPT_DIR}/.connection"

    # Return minimal output
    echo "[OK] PostgreSQL deployed (host: $host, port: $port)"

    return 0
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    init_log

    log_info "Starting PostgreSQL deployment to Kubernetes"
    log_info "Namespace: $NAMESPACE"
    log_info "Release: $RELEASE_NAME"
    log_info "Database: $DATABASE_NAME"

    # Step 1: Validate prerequisites
    if ! validate_prerequisites; then
        exit 2
    fi

    # Step 2: Ensure namespace exists
    if ! ensure_namespace; then
        exit 1
    fi

    # Step 3: Setup Helm repo
    if ! setup_helm_repo; then
        exit 1
    fi

    # Step 4: Deploy PostgreSQL
    if ! deploy_postgresql; then
        exit 1
    fi

    # Step 5: Wait for pod
    if ! wait_for_pod; then
        exit 1
    fi

    # Step 6: Get connection details
    if ! get_connection_details; then
        exit 1
    fi

    log_info "PostgreSQL deployment completed successfully"
    exit 0
}

main "$@"
