#!/usr/bin/env bash
# Deploy a FastAPI + Dapr service to Kubernetes.
#
# Usage: bash deploy_service.sh <service-name> [namespace]
# Example: bash deploy_service.sh triage-agent default

set -euo pipefail

SERVICE_NAME="${1:?ERROR: Service name required. Usage: deploy_service.sh <service-name> [namespace]}"
NAMESPACE="${2:-default}"
SERVICE_DIR="services/${SERVICE_NAME}"
K8S_DIR="${SERVICE_DIR}/k8s"
TIMEOUT=300  # 5 minutes

# ── Validate ─────────────────────────────────────────────────────────────────

if ! command -v kubectl &>/dev/null; then
    echo "ERROR: kubectl is not installed or not in PATH"
    exit 1
fi

if ! kubectl cluster-info &>/dev/null 2>&1; then
    echo "ERROR: Cannot connect to Kubernetes cluster"
    exit 1
fi

if ! command -v dapr &>/dev/null; then
    echo "ERROR: Dapr CLI is not installed or not in PATH"
    exit 1
fi

# Check Docker image exists
if ! docker image inspect "${SERVICE_NAME}:latest" &>/dev/null 2>&1; then
    echo "ERROR: Docker image ${SERVICE_NAME}:latest not found"
    echo "Run: bash scripts/build_docker.sh ${SERVICE_NAME} first"
    exit 1
fi

if [ ! -f "${K8S_DIR}/deployment.yaml" ]; then
    echo "ERROR: Kubernetes manifest not found at ${K8S_DIR}/deployment.yaml"
    echo "Run: python scripts/create_service.py --name ${SERVICE_NAME} --type <type> first"
    exit 1
fi

# ── Deploy Dapr Components (idempotent) ──────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAPR_CONFIG="${SCRIPT_DIR}/dapr_config.yaml"

if [ -f "${DAPR_CONFIG}" ]; then
    echo "Applying Dapr component configuration..."
    kubectl apply -f "${DAPR_CONFIG}" -n "${NAMESPACE}" 2>/dev/null || true
fi

# ── Deploy Service ───────────────────────────────────────────────────────────

echo "Deploying ${SERVICE_NAME} to namespace ${NAMESPACE}..."

# Apply manifest (--server-side for idempotent replace)
kubectl apply -f "${K8S_DIR}/deployment.yaml" -n "${NAMESPACE}"

# ── Wait for Ready ───────────────────────────────────────────────────────────

echo "Waiting for ${SERVICE_NAME} to be ready (timeout: ${TIMEOUT}s)..."

if kubectl rollout status deployment/"${SERVICE_NAME}" \
    -n "${NAMESPACE}" \
    --timeout="${TIMEOUT}s"; then
    echo "Service ${SERVICE_NAME} deployed successfully"
else
    echo "ERROR: Deployment timed out after ${TIMEOUT}s"
    echo "Pod status:"
    kubectl get pods -l app="${SERVICE_NAME}" -n "${NAMESPACE}"
    echo ""
    echo "Pod events:"
    kubectl describe pods -l app="${SERVICE_NAME}" -n "${NAMESPACE}" | tail -20
    exit 1
fi

# ── Verify Dapr Sidecar ─────────────────────────────────────────────────────

RETRY_COUNT=0
MAX_RETRIES=3

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    POD_NAME=$(kubectl get pods -l app="${SERVICE_NAME}" -n "${NAMESPACE}" \
        -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

    if [ -z "$POD_NAME" ]; then
        echo "WARNING: No pod found for ${SERVICE_NAME}, retrying..."
        RETRY_COUNT=$((RETRY_COUNT + 1))
        sleep 5
        continue
    fi

    SIDECAR_READY=$(kubectl get pod "$POD_NAME" -n "${NAMESPACE}" \
        -o jsonpath='{.status.containerStatuses[?(@.name=="daprd")].ready}' 2>/dev/null)

    if [ "$SIDECAR_READY" = "true" ]; then
        echo "Dapr sidecar is running for ${SERVICE_NAME}"
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
        echo "Dapr sidecar not ready, retrying (${RETRY_COUNT}/${MAX_RETRIES})..."
        sleep 10
    fi
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "WARNING: Dapr sidecar may not be ready after ${MAX_RETRIES} retries"
    echo "Check: kubectl logs ${POD_NAME} -c daprd -n ${NAMESPACE}"
fi

echo "Service ${SERVICE_NAME} deployed to ${NAMESPACE}"
