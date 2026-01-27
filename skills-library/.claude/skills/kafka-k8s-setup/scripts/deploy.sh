#!/usr/bin/env bash
#
# Kafka Kubernetes Deployment Script
#
# Deploys Apache Kafka to Kubernetes using Bitnami Helm chart with:
# - Prerequisites validation
# - Idempotent deployment
# - Zookeeper management
# - Retry logic with backoff
#
# Usage:
#   bash deploy.sh
#   NAMESPACE=myapp bash deploy.sh
#   DEBUG=1 bash deploy.sh
#
# Exit Codes:
#   0 - Success
#   1 - Fatal error
#   2 - Prerequisites not met

set -euo pipefail

# Configuration
NAMESPACE="${NAMESPACE:-kafka}"
RELEASE_NAME="${RELEASE_NAME:-kafka}"
CHART_VERSION="${CHART_VERSION:-28.3.0}"
HELM_TIMEOUT="${HELM_TIMEOUT:-5m}"
POD_WAIT_TIMEOUT="${POD_WAIT_TIMEOUT:-300}"  # 5 minutes
POD_CHECK_INTERVAL="${POD_CHECK_INTERVAL:-10}"  # seconds
MAX_RETRIES="${MAX_RETRIES:-3}"
RETRY_BACKOFF="${RETRY_BACKOFF:-30}"  # seconds
MIN_MEMORY_GB="${MIN_MEMORY_GB:-4}"

# Logging
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/.kafka-deploy.log"
DEBUG="${DEBUG:-0}"

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

# Initialize log
init_log() {
    echo "=== Kafka Deployment Started $(date -u +"%Y-%m-%dT%H:%M:%SZ") ===" >> "$LOG_FILE"
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

        local major minor
        major=$(echo "$helm_version" | cut -d. -f1 | tr -d 'v')
        minor=$(echo "$helm_version" | cut -d. -f2)
        if [[ "$major" -lt 3 ]] || { [[ "$major" -eq 3 ]] && [[ "$minor" -lt 9 ]]; }; then
            log_error "helm version $helm_version < 3.9 required"
            echo "[ERROR] helm 3.9+ required (found $helm_version)"
            ((errors++))
        fi
    fi

    # Check Kubernetes cluster
    if ! kubectl cluster-info &>/dev/null; then
        log_error "Kubernetes cluster not accessible"
        echo "[ERROR] Kubernetes not accessible"
        ((errors++))
    else
        local context
        context=$(kubectl config current-context 2>/dev/null || echo "unknown")
        log_debug "Kubernetes context: $context"
    fi

    # Check cluster resources (memory)
    if kubectl top nodes &>/dev/null 2>&1; then
        log_debug "Cluster metrics available"
    else
        log_warn "Cannot check cluster resources (metrics-server not installed)"
    fi

    # Check pod quotas
    local quota_check
    quota_check=$(kubectl get resourcequotas -A --no-headers 2>/dev/null | wc -l)
    if [[ "$quota_check" -gt 0 ]]; then
        log_debug "Resource quotas present, ensure sufficient pod count"
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

    if ! helm repo add bitnami https://charts.bitnami.com/bitnami 2>/dev/null; then
        log_debug "Bitnami repo may already exist, updating..."
    fi

    log_debug "Updating Helm repositories..."
    if ! helm repo update &>/dev/null; then
        log_warn "Helm repo update failed, continuing with cached charts"
    fi

    log_info "Helm repository ready"
    return 0
}

# =============================================================================
# KAFKA DEPLOYMENT
# =============================================================================

deploy_kafka() {
    log_info "Deploying Kafka..."

    local attempt=1
    local deployed=false

    while [[ $attempt -le $MAX_RETRIES ]]; do
        log_info "Deployment attempt $attempt of $MAX_RETRIES..."

        # Check if release exists
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
            helm "$cmd" "$RELEASE_NAME" bitnami/kafka
            --namespace "$NAMESPACE"
            --version "$CHART_VERSION"
            --set "listeners.client.protocol=PLAINTEXT"
            --set "listeners.controller.protocol=PLAINTEXT"
            --set "listeners.interbroker.protocol=PLAINTEXT"
            --set "controller.replicaCount=1"
            --set "persistence.enabled=true"
            --set "persistence.size=8Gi"
            --set "zookeeper.enabled=true"
            --set "zookeeper.replicaCount=1"
            --set "kraft.enabled=false"
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
# WAIT FOR PODS
# =============================================================================

wait_for_kafka_pods() {
    log_info "Waiting for Kafka pods to be ready..."

    local elapsed=0
    local kafka_ready=false
    local zk_ready=false

    while [[ $elapsed -lt $POD_WAIT_TIMEOUT ]]; do
        # Check Kafka pods
        local kafka_pods
        kafka_pods=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/component=kafka" \
            --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)

        # Check Zookeeper pods
        local zk_pods
        zk_pods=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/component=zookeeper" \
            --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)

        log_debug "Kafka pods: $kafka_pods, Zookeeper pods: $zk_pods ($elapsed/${POD_WAIT_TIMEOUT}s)"

        if [[ "$kafka_pods" -ge 1 ]]; then
            # Verify Kafka is ready
            local kafka_ready_status
            kafka_ready_status=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/component=kafka" \
                -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}' 2>/dev/null)
            if [[ "$kafka_ready_status" == *"True"* ]]; then
                kafka_ready=true
            fi
        fi

        if [[ "$zk_pods" -ge 1 ]]; then
            # Verify Zookeeper is ready
            local zk_ready_status
            zk_ready_status=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/component=zookeeper" \
                -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}' 2>/dev/null)
            if [[ "$zk_ready_status" == *"True"* ]]; then
                zk_ready=true
            fi
        fi

        if [[ "$kafka_ready" == "true" ]] && [[ "$zk_ready" == "true" ]]; then
            break
        fi

        sleep "$POD_CHECK_INTERVAL"
        ((elapsed += POD_CHECK_INTERVAL))
    done

    if [[ "$kafka_ready" != "true" ]] || [[ "$zk_ready" != "true" ]]; then
        log_error "Pods failed to become ready within ${POD_WAIT_TIMEOUT}s"
        kubectl get pods -n "$NAMESPACE" >> "$LOG_FILE" 2>&1
        kubectl describe pods -n "$NAMESPACE" >> "$LOG_FILE" 2>&1
        return 1
    fi

    log_info "Kafka and Zookeeper pods are ready"
    return 0
}

# =============================================================================
# CONNECTION DETAILS
# =============================================================================

get_connection_details() {
    log_info "Extracting connection details..."

    # Get Kafka service info
    local kafka_host="${RELEASE_NAME}.${NAMESPACE}.svc.cluster.local"
    local kafka_headless="${RELEASE_NAME}-headless.${NAMESPACE}.svc.cluster.local"
    local kafka_port=9092

    # Count pods
    local kafka_brokers
    kafka_brokers=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/component=kafka" \
        --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)

    local zk_nodes
    zk_nodes=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/component=zookeeper" \
        --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)

    log_debug "Kafka brokers: $kafka_brokers"
    log_debug "Zookeeper nodes: $zk_nodes"

    # Save connection info
    cat > "${SCRIPT_DIR}/.connection" << EOF
KAFKA_BOOTSTRAP_SERVERS=${kafka_headless}:${kafka_port}
KAFKA_HOST=${kafka_host}
KAFKA_PORT=${kafka_port}
KAFKA_NAMESPACE=${NAMESPACE}
KAFKA_BROKERS=${kafka_brokers}
ZOOKEEPER_NODES=${zk_nodes}
EOF

    log_info "Connection details saved to ${SCRIPT_DIR}/.connection"

    # Return minimal output
    echo "[OK] Kafka deployed (brokers: $kafka_brokers, zookeeper: $zk_nodes)"

    return 0
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    init_log

    log_info "Starting Kafka deployment to Kubernetes"
    log_info "Namespace: $NAMESPACE"
    log_info "Release: $RELEASE_NAME"

    # Step 1: Validate prerequisites
    if ! validate_prerequisites; then
        exit 2
    fi

    # Step 2: Ensure namespace
    if ! ensure_namespace; then
        exit 1
    fi

    # Step 3: Setup Helm repo
    if ! setup_helm_repo; then
        exit 1
    fi

    # Step 4: Deploy Kafka
    if ! deploy_kafka; then
        exit 1
    fi

    # Step 5: Wait for pods
    if ! wait_for_kafka_pods; then
        exit 1
    fi

    # Step 6: Get connection details
    if ! get_connection_details; then
        exit 1
    fi

    log_info "Kafka deployment completed successfully"
    exit 0
}

main "$@"
