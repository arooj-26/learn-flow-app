#!/usr/bin/env bash
#
# Build Docker Image for Next.js
#
# Creates an optimized multi-stage Docker image:
# - Stage 1: Install dependencies (cached)
# - Stage 2: Build application
# - Stage 3: Production runtime (~120-180MB)
#
# Usage:
#   bash scripts/build_docker.sh
#   IMAGE_NAME=myapp IMAGE_TAG=v1.0 bash scripts/build_docker.sh
#   REGISTRY=ghcr.io/org bash scripts/build_docker.sh
#
# Exit Codes:
#   0 - Success
#   1 - Fatal error (build failed)
#   2 - Prerequisites not met

set -euo pipefail

# ─── Configuration ────────────────────────────────────────────────────────────
PROJECT_NAME="${PROJECT_NAME:-frontend-app}"
PROJECT_DIR="${PROJECT_DIR:-./${PROJECT_NAME}}"
IMAGE_NAME="${IMAGE_NAME:-${PROJECT_NAME}}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
REGISTRY="${REGISTRY:-}"
PLATFORM="${PLATFORM:-linux/amd64}"
NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-/api}"
DEBUG="${DEBUG:-0}"
MAX_RETRIES="${MAX_RETRIES:-2}"
RETRY_BACKOFF="${RETRY_BACKOFF:-15}"

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
        log "ERROR" "build_docker.sh failed with exit code $exit_code"
        echo -e "${RED}[ERROR]${NC} Docker build failed. Check $LOG_FILE" >&2
    fi
}
trap cleanup EXIT

# ─── Validation ───────────────────────────────────────────────────────────────
validate() {
    local errors=0

    if ! command -v docker &>/dev/null; then
        log "ERROR" "Docker not found"
        ((errors++))
    elif ! docker info &>/dev/null 2>&1; then
        log "ERROR" "Docker daemon not running"
        ((errors++))
    fi

    if [[ ! -d "$PROJECT_DIR" ]]; then
        log "ERROR" "Project directory not found: $PROJECT_DIR"
        ((errors++))
    fi

    if [[ ! -f "$PROJECT_DIR/package.json" ]]; then
        log "ERROR" "package.json not found"
        ((errors++))
    fi

    if [[ $errors -gt 0 ]]; then
        echo "[ERROR] Prerequisites not met ($errors errors)" >&2
        exit 2
    fi
}

# ─── Generate Dockerfile ─────────────────────────────────────────────────────
generate_dockerfile() {
    # Only generate if Dockerfile doesn't exist
    if [[ -f "$PROJECT_DIR/Dockerfile" ]]; then
        log "INFO" "Dockerfile already exists, using existing"
        return 0
    fi

    log "INFO" "Generating Dockerfile..."

    cat > "$PROJECT_DIR/Dockerfile" << 'DOCKERFILE'
# ─── Stage 1: Dependencies ───────────────────────────────────────────────────
FROM node:18-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci --only=production --ignore-scripts 2>/dev/null || npm install --only=production

# ─── Stage 2: Build ──────────────────────────────────────────────────────────
FROM node:18-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

ARG NEXT_PUBLIC_API_URL=/api
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN npm run build

# ─── Stage 3: Production Runtime ─────────────────────────────────────────────
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy public assets
COPY --from=builder /app/public ./public

# Copy standalone build output
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
DOCKERFILE

    log "INFO" "Dockerfile generated"
}

# ─── Docker Build ─────────────────────────────────────────────────────────────
build_image() {
    local attempt=1

    while [[ $attempt -le $MAX_RETRIES ]]; do
        log "INFO" "Docker build attempt $attempt of $MAX_RETRIES..."
        log "INFO" "Image: $FULL_IMAGE | Platform: $PLATFORM"

        local build_start
        build_start=$(date +%s)

        if docker build \
            --platform "$PLATFORM" \
            --build-arg "NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL" \
            -t "$FULL_IMAGE" \
            -f "$PROJECT_DIR/Dockerfile" \
            "$PROJECT_DIR" >> "$LOG_FILE" 2>&1; then

            local build_end
            build_end=$(date +%s)
            local duration=$((build_end - build_start))
            log "INFO" "Docker build completed in ${duration}s"
            return 0
        fi

        log "WARN" "Docker build attempt $attempt failed"

        if [[ $attempt -lt $MAX_RETRIES ]]; then
            log "INFO" "Retrying in ${RETRY_BACKOFF}s..."
            sleep "$RETRY_BACKOFF"
        fi
        ((attempt++))
    done

    log "ERROR" "Docker build failed after $MAX_RETRIES attempts"
    return 1
}

# ─── Report ───────────────────────────────────────────────────────────────────
report_image_info() {
    local image_size
    image_size=$(docker images "$FULL_IMAGE" --format "{{.Size}}" 2>/dev/null | head -1)

    if [[ -z "$image_size" ]]; then
        image_size="unknown"
    fi

    log "INFO" "Image: $FULL_IMAGE ($image_size)"
    echo "[OK] Docker image built ($FULL_IMAGE, $image_size)"
}

# ─── Push (optional) ─────────────────────────────────────────────────────────
push_image() {
    if [[ -z "$REGISTRY" ]]; then
        log "DEBUG" "No registry configured, skipping push"
        return 0
    fi

    log "INFO" "Pushing image to registry..."
    if docker push "$FULL_IMAGE" >> "$LOG_FILE" 2>&1; then
        log "INFO" "Image pushed: $FULL_IMAGE"
    else
        log "WARN" "Image push failed (non-fatal)"
    fi
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
    log "INFO" "=== Docker Image Build ==="
    log "INFO" "Image: $FULL_IMAGE"

    validate
    generate_dockerfile
    build_image
    report_image_info
    push_image
}

main "$@"
