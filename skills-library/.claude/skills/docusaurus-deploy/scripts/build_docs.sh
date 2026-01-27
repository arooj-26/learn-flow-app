#!/usr/bin/env bash
# build_docs.sh - Production build for a Docusaurus documentation site.
#
# Cleans previous build artifacts, runs `npx docusaurus build`, and validates
# the output (index.html, sitemap.xml, size thresholds). Optionally runs bundle
# analysis and image optimization.
#
# Exit codes:
#   0 - Success
#   1 - Fatal error (build failed)
#   2 - Prerequisites not met
#   3 - Validation failed (output missing or exceeds thresholds)

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_DIR="${PROJECT_DIR:-.}"
BASE_URL="${BASE_URL:-/}"
ANALYZE_BUNDLE="${ANALYZE_BUNDLE:-0}"
ENABLE_PWA="${ENABLE_PWA:-false}"
OPTIMIZE_IMAGES="${OPTIMIZE_IMAGES:-0}"
NODE_ENV="${NODE_ENV:-production}"
MAX_BUILD_SIZE_MB="${MAX_BUILD_SIZE_MB:-20}"
MAX_ASSET_SIZE_MB="${MAX_ASSET_SIZE_MB:-5}"
LOG_FILE="${LOG_FILE:-.docusaurus-deploy.log}"
VERBOSE="${VERBOSE:-0}"

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
        log "ERROR" "build_docs.sh failed with exit code $exit_code"
    fi
}
trap cleanup EXIT

# ---------------------------------------------------------------------------
# Prerequisites
# ---------------------------------------------------------------------------
validate_prerequisites() {
    log "INFO" "Validating build prerequisites..."

    if [[ ! -d "$PROJECT_DIR" ]]; then
        log "ERROR" "Project directory not found: $PROJECT_DIR"
        exit 2
    fi

    if [[ ! -f "$PROJECT_DIR/docusaurus.config.js" ]]; then
        log "ERROR" "docusaurus.config.js not found in $PROJECT_DIR"
        exit 2
    fi

    if [[ ! -f "$PROJECT_DIR/package.json" ]]; then
        log "ERROR" "package.json not found in $PROJECT_DIR"
        exit 2
    fi

    if ! command -v npx &>/dev/null; then
        log "ERROR" "npx is not installed"
        exit 2
    fi

    # Ensure node_modules exist
    if [[ ! -d "$PROJECT_DIR/node_modules" ]]; then
        log "INFO" "node_modules not found – running npm install..."
        (cd "$PROJECT_DIR" && npm install) >> "$LOG_FILE" 2>&1
    fi

    log "INFO" "Build prerequisites OK"
}

# ---------------------------------------------------------------------------
# Clean previous build
# ---------------------------------------------------------------------------
clean_build() {
    log "INFO" "Cleaning previous build..."

    if [[ -d "$PROJECT_DIR/build" ]]; then
        rm -rf "$PROJECT_DIR/build"
        log "INFO" "Removed previous build directory"
    fi

    if [[ -d "$PROJECT_DIR/.docusaurus" ]]; then
        rm -rf "$PROJECT_DIR/.docusaurus"
        log "INFO" "Removed .docusaurus cache"
    fi
}

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
run_build() {
    log "INFO" "Running Docusaurus build..."

    local build_env="NODE_ENV=${NODE_ENV}"
    if [[ -n "$BASE_URL" ]] && [[ "$BASE_URL" != "/" ]]; then
        build_env="$build_env BASE_URL=${BASE_URL}"
    fi

    (cd "$PROJECT_DIR" && env $build_env npx docusaurus build) >> "$LOG_FILE" 2>&1

    if [[ $? -ne 0 ]]; then
        log "ERROR" "Docusaurus build failed"
        exit 1
    fi

    log "INFO" "Build complete"
}

# ---------------------------------------------------------------------------
# Bundle analysis
# ---------------------------------------------------------------------------
analyze_bundle() {
    if [[ "$ANALYZE_BUNDLE" != "1" ]]; then
        return 0
    fi

    log "INFO" "Running bundle analysis..."

    # Check if webpack-bundle-analyzer is available
    if (cd "$PROJECT_DIR" && npx --no -- webpack-bundle-analyzer --help) &>/dev/null; then
        (cd "$PROJECT_DIR" && npx docusaurus build --bundle-analyzer) >> "$LOG_FILE" 2>&1 || true
        log "INFO" "Bundle analysis complete (check browser for report)"
    else
        log "INFO" "webpack-bundle-analyzer not available – listing large files instead"
        if command -v du &>/dev/null; then
            log "INFO" "Largest build assets:"
            find "$PROJECT_DIR/build" -type f -name "*.js" -o -name "*.css" | \
                xargs du -h 2>/dev/null | sort -rh | head -10 >> "$LOG_FILE"
        fi
    fi
}

# ---------------------------------------------------------------------------
# Image optimization
# ---------------------------------------------------------------------------
optimize_images() {
    if [[ "$OPTIMIZE_IMAGES" != "1" ]]; then
        return 0
    fi

    log "INFO" "Optimizing images..."

    local build_img_dir="$PROJECT_DIR/build/img"
    if [[ ! -d "$build_img_dir" ]]; then
        log "INFO" "No img directory in build – skipping optimization"
        return 0
    fi

    # Try to use sharp-cli or imagemin if available
    if command -v npx &>/dev/null; then
        if (cd "$PROJECT_DIR" && npx --no -- sharp-cli --help) &>/dev/null; then
            log "INFO" "Using sharp-cli for image optimization"
            find "$build_img_dir" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | while read -r img; do
                npx sharp-cli -i "$img" -o "$img" --quality 80 >> "$LOG_FILE" 2>&1 || true
            done
        else
            log "INFO" "sharp-cli not available – skipping image optimization"
        fi
    fi
}

# ---------------------------------------------------------------------------
# Validate build output
# ---------------------------------------------------------------------------
validate_build() {
    log "INFO" "Validating build output..."
    local errors=0

    local build_dir="$PROJECT_DIR/build"

    # Check build directory exists
    if [[ ! -d "$build_dir" ]]; then
        log "ERROR" "Build directory does not exist: $build_dir"
        exit 3
    fi

    # Check index.html
    if [[ ! -f "$build_dir/index.html" ]]; then
        log "ERROR" "index.html not found in build output"
        ((errors++))
    fi

    # Check sitemap.xml
    if [[ ! -f "$build_dir/sitemap.xml" ]]; then
        log "WARN" "sitemap.xml not found in build output"
    fi

    # Check build size
    if command -v du &>/dev/null; then
        local build_size_kb
        build_size_kb=$(du -sk "$build_dir" 2>/dev/null | cut -f1)
        local max_size_kb=$((MAX_BUILD_SIZE_MB * 1024))

        if [[ "$build_size_kb" -gt "$max_size_kb" ]]; then
            log "ERROR" "Build size (${build_size_kb}KB) exceeds threshold (${max_size_kb}KB)"
            ((errors++))
        else
            log "INFO" "Build size: ${build_size_kb}KB (limit: ${max_size_kb}KB)"
        fi

        # Check largest asset
        local largest_asset_kb
        largest_asset_kb=$(find "$build_dir" -type f -exec du -k {} + 2>/dev/null | sort -rn | head -1 | cut -f1)
        local max_asset_kb=$((MAX_ASSET_SIZE_MB * 1024))

        if [[ -n "$largest_asset_kb" ]] && [[ "$largest_asset_kb" -gt "$max_asset_kb" ]]; then
            log "WARN" "Largest asset (${largest_asset_kb}KB) exceeds recommended threshold (${max_asset_kb}KB)"
        fi
    fi

    if [[ $errors -gt 0 ]]; then
        log "ERROR" "Build validation failed with $errors error(s)"
        exit 3
    fi

    log "INFO" "Build validation passed"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    log "INFO" "=== Documentation build started ==="
    log "INFO" "Project: $PROJECT_DIR | Base URL: $BASE_URL | Node env: $NODE_ENV"

    validate_prerequisites
    clean_build
    run_build
    analyze_bundle
    optimize_images
    validate_build

    # Compute final size for output
    local size_info=""
    if command -v du &>/dev/null; then
        local kb
        kb=$(du -sk "$PROJECT_DIR/build" 2>/dev/null | cut -f1)
        size_info=", size: ${kb}KB"
    fi

    log "INFO" "=== Documentation build complete ==="
    echo "[OK] Documentation built (dir: ${PROJECT_DIR}/build${size_info})"
}

main "$@"
