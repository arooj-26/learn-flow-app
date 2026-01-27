#!/usr/bin/env bash
#
# Build Next.js Frontend
#
# Runs production build with optimizations:
# - SWC minification
# - Standalone output mode
# - Bundle analysis (optional)
# - Build size validation
#
# Usage:
#   bash scripts/build_frontend.sh
#   ANALYZE_BUNDLE=1 bash scripts/build_frontend.sh
#   PROJECT_DIR=./myapp bash scripts/build_frontend.sh
#
# Exit Codes:
#   0 - Success
#   1 - Fatal error (build failed)
#   2 - Prerequisites not met
#   3 - Build warning (bundle size exceeded)

set -euo pipefail

# ─── Configuration ────────────────────────────────────────────────────────────
PROJECT_NAME="${PROJECT_NAME:-frontend-app}"
PROJECT_DIR="${PROJECT_DIR:-./${PROJECT_NAME}}"
NODE_ENV="${NODE_ENV:-production}"
NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-/api}"
ANALYZE_BUNDLE="${ANALYZE_BUNDLE:-0}"
DEBUG="${DEBUG:-0}"
BUILD_TIMEOUT="${BUILD_TIMEOUT:-600}"

# Bundle size thresholds (KB)
MAX_FIRST_LOAD_JS="${MAX_FIRST_LOAD_JS:-150}"
MAX_TOTAL_JS="${MAX_TOTAL_JS:-500}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${LOG_FILE:-${SCRIPT_DIR}/../.nextjs-k8s-deploy.log}"

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
    if [[ "$DEBUG" == "1" ]] || [[ "$level" == "ERROR" ]] || [[ "$level" == "WARN" ]]; then
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
    if [[ $exit_code -ne 0 ]] && [[ $exit_code -ne 3 ]]; then
        log "ERROR" "build_frontend.sh failed with exit code $exit_code"
        echo -e "${RED}[ERROR]${NC} Build failed. Check $LOG_FILE for details." >&2
    fi
}
trap cleanup EXIT

# ─── Validation ───────────────────────────────────────────────────────────────
validate() {
    local errors=0

    if [[ ! -d "$PROJECT_DIR" ]]; then
        log "ERROR" "Project directory not found: $PROJECT_DIR"
        ((errors++))
    fi

    if [[ ! -f "$PROJECT_DIR/package.json" ]]; then
        log "ERROR" "package.json not found in $PROJECT_DIR"
        ((errors++))
    fi

    if [[ ! -d "$PROJECT_DIR/node_modules" ]]; then
        log "WARN" "node_modules not found - running npm install..."
        (cd "$PROJECT_DIR" && npm install >> "$LOG_FILE" 2>&1) || {
            log "ERROR" "npm install failed"
            ((errors++))
        }
    fi

    if ! command -v node &>/dev/null; then
        log "ERROR" "Node.js not found"
        ((errors++))
    fi

    if [[ $errors -gt 0 ]]; then
        echo "[ERROR] Prerequisites not met ($errors errors)" >&2
        exit 2
    fi
}

# ─── Clean Previous Build ────────────────────────────────────────────────────
clean_build() {
    if [[ -d "$PROJECT_DIR/.next" ]]; then
        log "INFO" "Cleaning previous build..."
        rm -rf "$PROJECT_DIR/.next"
    fi
}

# ─── Build ────────────────────────────────────────────────────────────────────
run_build() {
    log "INFO" "Starting Next.js production build..."
    log "INFO" "NODE_ENV=$NODE_ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL"

    local build_start
    build_start=$(date +%s)

    local build_env="NODE_ENV=$NODE_ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL NEXT_TELEMETRY_DISABLED=1"

    if [[ "$ANALYZE_BUNDLE" == "1" ]]; then
        log "INFO" "Bundle analysis enabled"
        build_env="$build_env ANALYZE=true"
    fi

    if (cd "$PROJECT_DIR" && eval "$build_env npm run build" >> "$LOG_FILE" 2>&1); then
        local build_end
        build_end=$(date +%s)
        local build_duration=$((build_end - build_start))
        log "INFO" "Build completed in ${build_duration}s"
    else
        log "ERROR" "Next.js build failed"
        log "ERROR" "Last 30 lines of build output:"
        tail -30 "$LOG_FILE" >> "$LOG_FILE" 2>/dev/null
        echo "[ERROR] Next.js build failed. Run DEBUG=1 to see details." >&2
        exit 1
    fi
}

# ─── Validate Build Output ───────────────────────────────────────────────────
validate_build() {
    log "INFO" "Validating build output..."
    local warnings=0

    # Check .next directory exists
    if [[ ! -d "$PROJECT_DIR/.next" ]]; then
        log "ERROR" "Build output directory .next not found"
        exit 1
    fi

    # Check standalone output (if configured)
    if [[ -d "$PROJECT_DIR/.next/standalone" ]]; then
        log "INFO" "Standalone output found"
    else
        log "WARN" "Standalone output not found - Docker image will be larger"
        ((warnings++))
    fi

    # Estimate bundle size
    local total_js_size=0
    if [[ -d "$PROJECT_DIR/.next/static" ]]; then
        total_js_size=$(find "$PROJECT_DIR/.next/static" -name "*.js" -exec wc -c {} + 2>/dev/null | tail -1 | awk '{print int($1/1024)}')
        log "INFO" "Total JS bundle: ${total_js_size}KB"

        if [[ $total_js_size -gt $MAX_TOTAL_JS ]]; then
            log "WARN" "Total JS (${total_js_size}KB) exceeds threshold (${MAX_TOTAL_JS}KB)"
            ((warnings++))
        fi
    fi

    # Check for common issues
    if grep -r "console\.log" "$PROJECT_DIR/src" --include="*.ts" --include="*.tsx" -l 2>/dev/null | head -5 | grep -q .; then
        log "WARN" "console.log statements found in source files"
        ((warnings++))
    fi

    if [[ $warnings -gt 0 ]]; then
        log "WARN" "$warnings build warnings"
        return 3
    fi

    return 0
}

# ─── Report ───────────────────────────────────────────────────────────────────
report_build_info() {
    local build_size="unknown"

    if [[ -d "$PROJECT_DIR/.next" ]]; then
        build_size=$(du -sh "$PROJECT_DIR/.next" 2>/dev/null | awk '{print $1}')
    fi

    echo "[OK] Frontend build completed (${build_size} output)"
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
    log "INFO" "=== Next.js Frontend Build ==="
    log "INFO" "Project: $PROJECT_DIR"

    validate
    clean_build
    run_build

    local exit_code=0
    validate_build || exit_code=$?

    report_build_info

    exit $exit_code
}

main "$@"
