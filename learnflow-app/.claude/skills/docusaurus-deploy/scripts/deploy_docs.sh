#!/usr/bin/env bash
# deploy_docs.sh - Deploy Docusaurus documentation to various targets.
#
# Supports 4 deployment targets:
#   - github-pages: Uses `npx docusaurus deploy` or manual gh-pages push
#   - vercel: Uses `vercel --prod` with vercel.json
#   - netlify: Uses `netlify deploy --prod` with netlify.toml
#   - k8s: Docker multi-stage build + nginx + Kubernetes deployment
#
# Optionally generates a CI/CD GitHub Actions workflow (GENERATE_CI=1).
#
# Exit codes:
#   0 - Success
#   1 - Fatal error
#   2 - Prerequisites not met
#   3 - Deployment failed (after retries)
#   4 - Configuration error

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEPLOY_TARGET="${DEPLOY_TARGET:-github-pages}"
PROJECT_DIR="${PROJECT_DIR:-.}"
MAX_RETRIES="${MAX_RETRIES:-3}"
RETRY_BACKOFF="${RETRY_BACKOFF:-5}"
GENERATE_CI="${GENERATE_CI:-0}"
LOG_FILE="${LOG_FILE:-.docusaurus-deploy.log}"
VERBOSE="${VERBOSE:-0}"

# GitHub Pages
GH_PAGES_BRANCH="${GH_PAGES_BRANCH:-gh-pages}"
GIT_USER="${GIT_USER:-}"
GIT_PASS="${GIT_PASS:-}"
DEPLOYMENT_BRANCH="${DEPLOYMENT_BRANCH:-gh-pages}"

# Vercel
VERCEL_TOKEN="${VERCEL_TOKEN:-}"
VERCEL_ORG_ID="${VERCEL_ORG_ID:-}"
VERCEL_PROJECT_ID="${VERCEL_PROJECT_ID:-}"

# Netlify
NETLIFY_TOKEN="${NETLIFY_TOKEN:-}"
NETLIFY_SITE_ID="${NETLIFY_SITE_ID:-}"

# Kubernetes
NAMESPACE="${NAMESPACE:-docs}"
IMAGE_NAME="${IMAGE_NAME:-docs-site}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
REGISTRY="${REGISTRY:-}"
REPLICAS="${REPLICAS:-2}"
NODE_PORT="${NODE_PORT:-30080}"
CONTAINER_PORT="${CONTAINER_PORT:-80}"

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

cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        log "ERROR" "deploy_docs.sh failed with exit code $exit_code"
    fi
}
trap cleanup EXIT

# ---------------------------------------------------------------------------
# Retry helper
# ---------------------------------------------------------------------------
retry_command() {
    local desc="$1"; shift
    local attempt=1

    while [[ $attempt -le $MAX_RETRIES ]]; do
        log "INFO" "Attempt $attempt/$MAX_RETRIES: $desc"
        if "$@"; then
            return 0
        fi
        log "WARN" "Attempt $attempt failed for: $desc"
        if [[ $attempt -lt $MAX_RETRIES ]]; then
            local wait=$((RETRY_BACKOFF * attempt))
            log "INFO" "Retrying in ${wait}s..."
            sleep "$wait"
        fi
        ((attempt++))
    done

    log "ERROR" "All $MAX_RETRIES attempts failed for: $desc"
    return 1
}

# ---------------------------------------------------------------------------
# GitHub Pages deployment
# ---------------------------------------------------------------------------
deploy_github_pages() {
    log "INFO" "Deploying to GitHub Pages..."

    if ! command -v npx &>/dev/null; then
        log "ERROR" "npx is required for GitHub Pages deployment"
        exit 2
    fi

    local deploy_env=""
    if [[ -n "$GIT_USER" ]]; then
        deploy_env="GIT_USER=${GIT_USER}"
    fi
    if [[ -n "$GIT_PASS" ]]; then
        deploy_env="$deploy_env GIT_PASS=${GIT_PASS}"
    fi

    local deploy_cmd="cd \"$PROJECT_DIR\" && ${deploy_env:+env $deploy_env }npx docusaurus deploy"

    if ! retry_command "GitHub Pages deploy" bash -c "$deploy_cmd" >> "$LOG_FILE" 2>&1; then
        # Fallback: manual gh-pages push
        log "INFO" "Falling back to manual gh-pages push..."
        if command -v gh &>/dev/null; then
            (cd "$PROJECT_DIR" && gh-pages -d build -b "$GH_PAGES_BRANCH") >> "$LOG_FILE" 2>&1 || {
                log "ERROR" "GitHub Pages deployment failed"
                exit 3
            }
        else
            log "ERROR" "GitHub Pages deployment failed and gh CLI not available for fallback"
            exit 3
        fi
    fi

    log "INFO" "GitHub Pages deployment complete"
}

# ---------------------------------------------------------------------------
# Vercel deployment
# ---------------------------------------------------------------------------
deploy_vercel() {
    log "INFO" "Deploying to Vercel..."

    if ! command -v vercel &>/dev/null && ! command -v npx &>/dev/null; then
        log "ERROR" "vercel CLI or npx is required"
        exit 2
    fi

    # Generate vercel.json if it doesn't exist
    local vercel_config="$PROJECT_DIR/vercel.json"
    if [[ ! -f "$vercel_config" ]]; then
        log "INFO" "Generating vercel.json..."
        cat > "$vercel_config" << 'VERCELEOF'
{
  "buildCommand": "npx docusaurus build",
  "outputDirectory": "build",
  "framework": "docusaurus-2",
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
VERCELEOF
    fi

    local vercel_cmd="vercel"
    if ! command -v vercel &>/dev/null; then
        vercel_cmd="npx vercel"
    fi

    local token_flag=""
    if [[ -n "$VERCEL_TOKEN" ]]; then
        token_flag="--token $VERCEL_TOKEN"
    fi

    if ! retry_command "Vercel deploy" bash -c \
        "cd \"$PROJECT_DIR\" && $vercel_cmd --prod --yes $token_flag" >> "$LOG_FILE" 2>&1; then
        log "ERROR" "Vercel deployment failed"
        exit 3
    fi

    log "INFO" "Vercel deployment complete"
}

# ---------------------------------------------------------------------------
# Netlify deployment
# ---------------------------------------------------------------------------
deploy_netlify() {
    log "INFO" "Deploying to Netlify..."

    if ! command -v netlify &>/dev/null && ! command -v npx &>/dev/null; then
        log "ERROR" "netlify CLI or npx is required"
        exit 2
    fi

    # Generate netlify.toml if it doesn't exist
    local netlify_config="$PROJECT_DIR/netlify.toml"
    if [[ ! -f "$netlify_config" ]]; then
        log "INFO" "Generating netlify.toml..."
        cat > "$netlify_config" << 'NETLIFYEOF'
[build]
  publish = "build"
  command = "npx docusaurus build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.html"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"
NETLIFYEOF
    fi

    local netlify_cmd="netlify"
    if ! command -v netlify &>/dev/null; then
        netlify_cmd="npx netlify-cli"
    fi

    local token_flag=""
    if [[ -n "$NETLIFY_TOKEN" ]]; then
        token_flag="--auth $NETLIFY_TOKEN"
    fi

    local site_flag=""
    if [[ -n "$NETLIFY_SITE_ID" ]]; then
        site_flag="--site $NETLIFY_SITE_ID"
    fi

    if ! retry_command "Netlify deploy" bash -c \
        "cd \"$PROJECT_DIR\" && $netlify_cmd deploy --prod --dir=build $token_flag $site_flag" >> "$LOG_FILE" 2>&1; then
        log "ERROR" "Netlify deployment failed"
        exit 3
    fi

    log "INFO" "Netlify deployment complete"
}

# ---------------------------------------------------------------------------
# Kubernetes deployment
# ---------------------------------------------------------------------------
deploy_k8s() {
    log "INFO" "Deploying to Kubernetes..."

    if ! command -v docker &>/dev/null; then
        log "ERROR" "docker is required for K8s deployment"
        exit 2
    fi
    if ! command -v kubectl &>/dev/null; then
        log "ERROR" "kubectl is required for K8s deployment"
        exit 2
    fi

    local full_image="${IMAGE_NAME}:${IMAGE_TAG}"
    if [[ -n "$REGISTRY" ]]; then
        full_image="${REGISTRY}/${full_image}"
    fi

    # Generate Dockerfile
    local dockerfile="$PROJECT_DIR/Dockerfile"
    if [[ ! -f "$dockerfile" ]]; then
        log "INFO" "Generating multi-stage Dockerfile..."
        cat > "$dockerfile" << 'DOCKEREOF'
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production=false
COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY <<'NGINXCONF' /etc/nginx/conf.d/default.conf
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;
}
NGINXCONF
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
DOCKEREOF
    fi

    # Build Docker image
    log "INFO" "Building Docker image: $full_image"
    if ! retry_command "Docker build" docker build -t "$full_image" "$PROJECT_DIR" >> "$LOG_FILE" 2>&1; then
        log "ERROR" "Docker build failed"
        exit 3
    fi

    # Push to registry if specified
    if [[ -n "$REGISTRY" ]]; then
        log "INFO" "Pushing image to registry..."
        if ! retry_command "Docker push" docker push "$full_image" >> "$LOG_FILE" 2>&1; then
            log "ERROR" "Docker push failed"
            exit 3
        fi
    fi

    # Create namespace
    kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f - >> "$LOG_FILE" 2>&1

    # Generate K8s manifests
    local k8s_dir="$PROJECT_DIR/k8s"
    mkdir -p "$k8s_dir"

    # ConfigMap
    cat > "$k8s_dir/configmap.yaml" << CMEOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${IMAGE_NAME}-config
  namespace: ${NAMESPACE}
data:
  NGINX_PORT: "${CONTAINER_PORT}"
CMEOF

    # Deployment
    cat > "$k8s_dir/deployment.yaml" << DEPEOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${IMAGE_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${IMAGE_NAME}
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: ${IMAGE_NAME}
  template:
    metadata:
      labels:
        app: ${IMAGE_NAME}
    spec:
      containers:
        - name: ${IMAGE_NAME}
          image: ${full_image}
          ports:
            - containerPort: ${CONTAINER_PORT}
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
          livenessProbe:
            httpGet:
              path: /
              port: ${CONTAINER_PORT}
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: ${CONTAINER_PORT}
            initialDelaySeconds: 3
            periodSeconds: 5
DEPEOF

    # Service
    cat > "$k8s_dir/service.yaml" << SVCEOF
apiVersion: v1
kind: Service
metadata:
  name: ${IMAGE_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${IMAGE_NAME}
spec:
  type: NodePort
  selector:
    app: ${IMAGE_NAME}
  ports:
    - port: ${CONTAINER_PORT}
      targetPort: ${CONTAINER_PORT}
      nodePort: ${NODE_PORT}
      protocol: TCP
SVCEOF

    # Apply manifests
    log "INFO" "Applying Kubernetes manifests..."
    if ! retry_command "K8s apply" kubectl apply -f "$k8s_dir/" >> "$LOG_FILE" 2>&1; then
        log "ERROR" "Kubernetes deployment failed"
        exit 3
    fi

    # Wait for rollout
    log "INFO" "Waiting for rollout to complete..."
    kubectl rollout status deployment/"$IMAGE_NAME" -n "$NAMESPACE" --timeout=120s >> "$LOG_FILE" 2>&1 || {
        log "WARN" "Rollout did not complete within timeout"
    }

    log "INFO" "Kubernetes deployment complete (namespace: $NAMESPACE, nodePort: $NODE_PORT)"
}

# ---------------------------------------------------------------------------
# Generate CI/CD workflow
# ---------------------------------------------------------------------------
generate_ci_workflow() {
    if [[ "$GENERATE_CI" != "1" ]]; then
        return 0
    fi

    log "INFO" "Generating CI/CD workflow..."

    local workflows_dir="$PROJECT_DIR/.github/workflows"
    mkdir -p "$workflows_dir"

    cat > "$workflows_dir/deploy-docs.yml" << 'CIEOF'
name: Deploy Documentation

on:
  push:
    branches: [main, master]
    paths:
      - 'docs/**'
      - 'src/**'
      - 'docusaurus.config.js'
      - 'sidebars.js'
      - 'package.json'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build documentation
        run: npx docusaurus build
        env:
          NODE_ENV: production

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
CIEOF

    log "INFO" "CI/CD workflow generated at $workflows_dir/deploy-docs.yml"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    log "INFO" "=== Documentation deployment started ==="
    log "INFO" "Target: $DEPLOY_TARGET | Project: $PROJECT_DIR"

    # Validate build exists
    if [[ ! -d "$PROJECT_DIR/build" ]]; then
        log "ERROR" "Build directory not found. Run build_docs.sh first."
        exit 2
    fi

    case "$DEPLOY_TARGET" in
        github-pages)
            deploy_github_pages
            ;;
        vercel)
            deploy_vercel
            ;;
        netlify)
            deploy_netlify
            ;;
        k8s|kubernetes)
            deploy_k8s
            ;;
        *)
            log "ERROR" "Unknown deploy target: $DEPLOY_TARGET (expected: github-pages, vercel, netlify, k8s)"
            exit 4
            ;;
    esac

    generate_ci_workflow

    log "INFO" "=== Documentation deployment complete ==="
    echo "[OK] Documentation deployed (target: ${DEPLOY_TARGET})"
}

main "$@"
