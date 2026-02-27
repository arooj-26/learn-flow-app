#!/usr/bin/env bash
# Build Docker image for a FastAPI + Dapr service.
#
# Usage: bash build_docker.sh <service-name> [version]
# Example: bash build_docker.sh triage-agent 1.0.0

set -euo pipefail

SERVICE_NAME="${1:?ERROR: Service name required. Usage: build_docker.sh <service-name> [version]}"
VERSION="${2:-latest}"
SERVICE_DIR="services/${SERVICE_NAME}"
MAX_IMAGE_SIZE_MB=500

# ── Validate ─────────────────────────────────────────────────────────────────

if ! command -v docker &>/dev/null; then
    echo "ERROR: Docker is not installed or not in PATH"
    exit 1
fi

if [ ! -f "${SERVICE_DIR}/Dockerfile" ]; then
    echo "ERROR: Dockerfile not found at ${SERVICE_DIR}/Dockerfile"
    echo "Run: python scripts/create_service.py --name ${SERVICE_NAME} --type <type> first"
    exit 1
fi

if [ ! -f "${SERVICE_DIR}/requirements.txt" ]; then
    echo "ERROR: requirements.txt not found at ${SERVICE_DIR}/requirements.txt"
    exit 1
fi

if [ ! -f "${SERVICE_DIR}/main.py" ]; then
    echo "ERROR: main.py not found at ${SERVICE_DIR}/main.py"
    exit 1
fi

# ── Build ────────────────────────────────────────────────────────────────────

echo "Building ${SERVICE_NAME}:${VERSION}..."

docker build \
    -t "${SERVICE_NAME}:${VERSION}" \
    -t "${SERVICE_NAME}:latest" \
    --label "app=${SERVICE_NAME}" \
    --label "version=${VERSION}" \
    --label "built-at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    "${SERVICE_DIR}"

# ── Validate Image Size ─────────────────────────────────────────────────────

IMAGE_SIZE_BYTES=$(docker inspect "${SERVICE_NAME}:${VERSION}" --format='{{.Size}}')
IMAGE_SIZE_MB=$((IMAGE_SIZE_BYTES / 1024 / 1024))

if [ "${IMAGE_SIZE_MB}" -gt "${MAX_IMAGE_SIZE_MB}" ]; then
    echo "WARNING: Image size ${IMAGE_SIZE_MB}MB exceeds ${MAX_IMAGE_SIZE_MB}MB limit"
    echo "Consider optimizing Dockerfile (multi-stage build, smaller base image)"
fi

echo "Image size: ${IMAGE_SIZE_MB}MB"
echo "Service ${SERVICE_NAME}:${VERSION} built successfully"
