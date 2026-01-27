#!/usr/bin/env bash
#
# Deploy Next.js to Kubernetes
#
# Creates Kubernetes resources for the Next.js application:
# - Namespace (if not exists)
# - ConfigMap for environment variables
# - Deployment with rolling update strategy
# - Service (NodePort)
# - Health probes (startup, liveness, readiness)
#
# Idempotent: safe to run multiple times.
#
# Usage:
#   bash scripts/deploy_k8s.sh
#   NAMESPACE=staging REPLICAS=3 bash scripts/deploy_k8s.sh
#   IMAGE_TAG=v1.2.0 bash scripts/deploy_k8s.sh
#
# Exit Codes:
#   0 - Success
#   1 - Fatal error
#   2 - Prerequisites not met (retryable)
#   4 - Health check timeout

set -euo pipefail

# ─── Configuration ────────────────────────────────────────────────────────────
NAMESPACE="${NAMESPACE:-frontend}"
RELEASE_NAME="${RELEASE_NAME:-frontend-app}"
IMAGE_NAME="${IMAGE_NAME:-frontend-app}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
REGISTRY="${REGISTRY:-}"
REPLICAS="${REPLICAS:-2}"
API_BACKEND_URL="${API_BACKEND_URL:-http://api-svc:8000}"
NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-/api}"
PORT="${PORT:-3000}"
NODE_PORT="${NODE_PORT:-30080}"
CPU_REQUEST="${CPU_REQUEST:-100m}"
CPU_LIMIT="${CPU_LIMIT:-500m}"
MEM_REQUEST="${MEM_REQUEST:-128Mi}"
MEM_LIMIT="${MEM_LIMIT:-512Mi}"
MAX_RETRIES="${MAX_RETRIES:-3}"
RETRY_BACKOFF="${RETRY_BACKOFF:-15}"
ROLLOUT_TIMEOUT="${ROLLOUT_TIMEOUT:-180}"
DEBUG="${DEBUG:-0}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${LOG_FILE:-${SCRIPT_DIR}/../.nextjs-k8s-deploy.log}"

# Full image reference
if [[ -n "$REGISTRY" ]]; then
    FULL_IMAGE="${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
else
    FULL_IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"
fi

# Colors
if [[ -t 1 ]]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; NC=''
fi

log() {
    local level="$1"; shift
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")
    echo "[$timestamp] [$level] $*" >> "$LOG_FILE"
    if [[ "$DEBUG" == "1" ]] || [[ "$level" == "ERROR" ]]; then
        case "$level" in
            ERROR) echo -e "${RED}[ERROR]${NC} $*" >&2 ;;
            WARN)  echo -e "${YELLOW}[WARN]${NC} $*" >&2 ;;
            INFO)  echo -e "${GREEN}[INFO]${NC} $*" ;;
            DEBUG) [[ "$DEBUG" == "1" ]] && echo "[DEBUG] $*" ;;
        esac
    fi
}

cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        log "ERROR" "deploy_k8s.sh failed with exit code $exit_code"
        echo -e "${RED}[ERROR]${NC} Deployment failed. Check $LOG_FILE" >&2
    fi
}
trap cleanup EXIT

# ─── Prerequisites ────────────────────────────────────────────────────────────
validate_prerequisites() {
    log "INFO" "Validating prerequisites..."
    local errors=0

    if ! command -v kubectl &>/dev/null; then
        log "ERROR" "kubectl not found"
        ((errors++))
    fi

    if ! kubectl cluster-info &>/dev/null 2>&1; then
        log "ERROR" "Kubernetes cluster not accessible"
        ((errors++))
    fi

    # Verify image exists locally or is pullable
    if [[ -z "$REGISTRY" ]]; then
        if ! docker image inspect "$FULL_IMAGE" &>/dev/null 2>&1; then
            log "WARN" "Image $FULL_IMAGE not found locally"
        fi
    fi

    if [[ $errors -gt 0 ]]; then
        echo "[ERROR] Prerequisites not met ($errors errors)" >&2
        exit 2
    fi
    log "INFO" "Prerequisites validated"
}

# ─── Namespace ────────────────────────────────────────────────────────────────
ensure_namespace() {
    if kubectl get namespace "$NAMESPACE" &>/dev/null 2>&1; then
        log "DEBUG" "Namespace $NAMESPACE already exists"
    else
        log "INFO" "Creating namespace $NAMESPACE..."
        kubectl create namespace "$NAMESPACE" >> "$LOG_FILE" 2>&1
        log "INFO" "Namespace $NAMESPACE created"
    fi
}

# ─── ConfigMap ────────────────────────────────────────────────────────────────
apply_configmap() {
    log "INFO" "Applying ConfigMap..."

    cat << EOF | kubectl apply -n "$NAMESPACE" -f - >> "$LOG_FILE" 2>&1
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${RELEASE_NAME}-config
  namespace: ${NAMESPACE}
  labels:
    app: ${RELEASE_NAME}
data:
  NODE_ENV: "production"
  NEXT_PUBLIC_API_URL: "${NEXT_PUBLIC_API_URL}"
  API_BACKEND_URL: "${API_BACKEND_URL}"
  PORT: "${PORT}"
EOF

    log "INFO" "ConfigMap applied"
}

# ─── Deployment ───────────────────────────────────────────────────────────────
apply_deployment() {
    log "INFO" "Applying Deployment (image: $FULL_IMAGE, replicas: $REPLICAS)..."

    cat << EOF | kubectl apply -n "$NAMESPACE" -f - >> "$LOG_FILE" 2>&1
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${RELEASE_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${RELEASE_NAME}
    version: "${IMAGE_TAG}"
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: ${RELEASE_NAME}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  minReadySeconds: 5
  progressDeadlineSeconds: 300
  template:
    metadata:
      labels:
        app: ${RELEASE_NAME}
        version: "${IMAGE_TAG}"
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        runAsGroup: 1001
        fsGroup: 1001
      containers:
        - name: nextjs
          image: ${FULL_IMAGE}
          imagePullPolicy: ${REGISTRY:+Always}${REGISTRY:-IfNotPresent}
          ports:
            - name: http
              containerPort: ${PORT}
              protocol: TCP
          envFrom:
            - configMapRef:
                name: ${RELEASE_NAME}-config
          resources:
            requests:
              cpu: ${CPU_REQUEST}
              memory: ${MEM_REQUEST}
            limits:
              cpu: ${CPU_LIMIT}
              memory: ${MEM_LIMIT}
          startupProbe:
            httpGet:
              path: /api/health
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 30
            timeoutSeconds: 3
          livenessProbe:
            httpGet:
              path: /api/health
              port: http
            periodSeconds: 30
            failureThreshold: 3
            timeoutSeconds: 5
          readinessProbe:
            httpGet:
              path: /api/health
              port: http
            periodSeconds: 10
            failureThreshold: 3
            timeoutSeconds: 3
      terminationGracePeriodSeconds: 30
EOF

    log "INFO" "Deployment applied"
}

# ─── Service ──────────────────────────────────────────────────────────────────
apply_service() {
    log "INFO" "Applying Service (NodePort: $NODE_PORT)..."

    cat << EOF | kubectl apply -n "$NAMESPACE" -f - >> "$LOG_FILE" 2>&1
apiVersion: v1
kind: Service
metadata:
  name: ${RELEASE_NAME}-svc
  namespace: ${NAMESPACE}
  labels:
    app: ${RELEASE_NAME}
spec:
  type: NodePort
  selector:
    app: ${RELEASE_NAME}
  ports:
    - name: http
      port: 80
      targetPort: ${PORT}
      nodePort: ${NODE_PORT}
      protocol: TCP
EOF

    log "INFO" "Service applied"
}

# ─── Wait for Rollout ─────────────────────────────────────────────────────────
wait_for_rollout() {
    log "INFO" "Waiting for rollout to complete (timeout: ${ROLLOUT_TIMEOUT}s)..."

    if kubectl rollout status deployment/"$RELEASE_NAME" \
        -n "$NAMESPACE" \
        --timeout="${ROLLOUT_TIMEOUT}s" >> "$LOG_FILE" 2>&1; then
        log "INFO" "Rollout completed successfully"
        return 0
    else
        log "ERROR" "Rollout did not complete within ${ROLLOUT_TIMEOUT}s"

        # Capture pod status for diagnostics
        log "ERROR" "Pod status:"
        kubectl get pods -n "$NAMESPACE" -l "app=$RELEASE_NAME" -o wide >> "$LOG_FILE" 2>&1

        # Capture events
        log "ERROR" "Recent events:"
        kubectl get events -n "$NAMESPACE" --sort-by='.lastTimestamp' \
            --field-selector "involvedObject.name=$RELEASE_NAME" >> "$LOG_FILE" 2>&1 || true

        return 4
    fi
}

# ─── Health Check ─────────────────────────────────────────────────────────────
health_check() {
    log "INFO" "Running health check..."
    local attempt=1
    local max_attempts=5
    local delay=5

    while [[ $attempt -le $max_attempts ]]; do
        local pod
        pod=$(kubectl get pods -n "$NAMESPACE" -l "app=$RELEASE_NAME" \
            --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")

        if [[ -n "$pod" ]]; then
            local health_response
            health_response=$(kubectl exec -n "$NAMESPACE" "$pod" -- \
                wget -q -O - "http://localhost:${PORT}/api/health" 2>/dev/null || echo "")

            if echo "$health_response" | grep -q '"status"' 2>/dev/null; then
                log "INFO" "Health check passed: $health_response"
                return 0
            fi
        fi

        log "DEBUG" "Health check attempt $attempt failed, retrying in ${delay}s..."
        sleep "$delay"
        ((attempt++))
    done

    log "WARN" "Health check failed after $max_attempts attempts"
    return 4
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
    log "INFO" "=== Kubernetes Deployment ==="
    log "INFO" "Namespace: $NAMESPACE | Release: $RELEASE_NAME | Image: $FULL_IMAGE"

    validate_prerequisites
    ensure_namespace
    apply_configmap
    apply_deployment
    apply_service
    wait_for_rollout

    local exit_code=0
    health_check || exit_code=$?

    # Get final pod count
    local ready_pods
    ready_pods=$(kubectl get deployment "$RELEASE_NAME" -n "$NAMESPACE" \
        -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")

    echo "[OK] Deployed to Kubernetes ($NAMESPACE/$RELEASE_NAME, ${ready_pods:-0} replicas)"

    exit $exit_code
}

main "$@"
