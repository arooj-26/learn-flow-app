#!/usr/bin/env bash
#
# Initialize Next.js Project
#
# Creates a production-grade Next.js project with TypeScript, Tailwind CSS,
# App Router, and essential dependencies pre-configured.
#
# Usage:
#   bash scripts/init_nextjs.sh
#   PROJECT_NAME=myapp bash scripts/init_nextjs.sh
#   DEBUG=1 bash scripts/init_nextjs.sh
#
# Exit Codes:
#   0 - Success
#   1 - Fatal error
#   2 - Prerequisites not met (retryable)

set -euo pipefail

# ─── Configuration ────────────────────────────────────────────────────────────
PROJECT_NAME="${PROJECT_NAME:-frontend-app}"
PROJECT_DIR="${PROJECT_DIR:-./${PROJECT_NAME}}"
NODE_ENV="${NODE_ENV:-development}"
DEBUG="${DEBUG:-0}"
MAX_RETRIES="${MAX_RETRIES:-2}"
RETRY_BACKOFF="${RETRY_BACKOFF:-15}"
NPM_INSTALL_TIMEOUT="${NPM_INSTALL_TIMEOUT:-300}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${LOG_FILE:-${SCRIPT_DIR}/../.nextjs-k8s-deploy.log}"

# Colors
if [[ -t 1 ]]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; NC=''
fi

# ─── Logging ──────────────────────────────────────────────────────────────────
log() {
    local level="$1"; shift
    local message="$*"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"

    if [[ "$DEBUG" == "1" ]] || [[ "$level" == "ERROR" ]]; then
        case "$level" in
            ERROR) echo -e "${RED}[ERROR]${NC} $message" >&2 ;;
            WARN)  echo -e "${YELLOW}[WARN]${NC} $message" >&2 ;;
            INFO)  echo -e "${GREEN}[INFO]${NC} $message" ;;
            DEBUG) [[ "$DEBUG" == "1" ]] && echo "[DEBUG] $message" ;;
        esac
    fi
}

cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        log "ERROR" "init_nextjs.sh failed with exit code $exit_code"
        echo -e "${RED}[ERROR]${NC} Initialization failed. Check $LOG_FILE for details." >&2
    fi
}
trap cleanup EXIT

# ─── Prerequisites ────────────────────────────────────────────────────────────
validate_prerequisites() {
    log "INFO" "Validating prerequisites..."
    local errors=0

    if ! command -v node &>/dev/null; then
        log "ERROR" "Node.js not found. Install Node.js >= 18"
        ((errors++))
    else
        local node_version
        node_version=$(node --version | sed 's/v//')
        local node_major
        node_major=$(echo "$node_version" | cut -d. -f1)
        if [[ "$node_major" -lt 18 ]]; then
            log "ERROR" "Node.js >= 18 required (found v${node_version})"
            ((errors++))
        fi
        log "DEBUG" "Node.js v${node_version}"
    fi

    if ! command -v npm &>/dev/null; then
        log "ERROR" "npm not found"
        ((errors++))
    else
        log "DEBUG" "npm $(npm --version)"
    fi

    if [[ $errors -gt 0 ]]; then
        echo "[ERROR] Prerequisites not met ($errors errors)" >&2
        return 2
    fi
    log "INFO" "Prerequisites validated"
    return 0
}

# ─── Idempotency Check ───────────────────────────────────────────────────────
check_existing_project() {
    if [[ -d "$PROJECT_DIR" ]] && [[ -f "$PROJECT_DIR/package.json" ]]; then
        local existing_name
        existing_name=$(node -e "console.log(require('$PROJECT_DIR/package.json').name || '')" 2>/dev/null || echo "")
        if [[ -n "$existing_name" ]]; then
            log "INFO" "Project already exists at $PROJECT_DIR (name: $existing_name)"
            # Verify dependencies are installed
            if [[ -d "$PROJECT_DIR/node_modules" ]]; then
                echo "[OK] Next.js project already initialized ($PROJECT_DIR)"
                return 0
            else
                log "WARN" "node_modules missing - will reinstall dependencies"
                return 1
            fi
        fi
    fi
    return 1
}

# ─── Project Creation ────────────────────────────────────────────────────────
create_project() {
    log "INFO" "Creating Next.js project: $PROJECT_NAME at $PROJECT_DIR"

    mkdir -p "$(dirname "$PROJECT_DIR")"

    # Create package.json
    mkdir -p "$PROJECT_DIR"
    cat > "$PROJECT_DIR/package.json" << 'PKGJSON'
{
  "name": "PROJECT_NAME_PLACEHOLDER",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "analyze": "ANALYZE=true next build"
  }
}
PKGJSON

    # Replace placeholder
    if command -v sed &>/dev/null; then
        sed -i "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/g" "$PROJECT_DIR/package.json" 2>/dev/null || \
        sed -i '' "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/g" "$PROJECT_DIR/package.json" 2>/dev/null || true
    fi

    log "INFO" "Installing dependencies..."
    install_dependencies

    # Create project structure
    create_project_structure
    create_config_files
    create_health_endpoint

    log "INFO" "Project initialization complete"
}

install_dependencies() {
    local attempt=1

    # Core dependencies
    local deps=(
        "next@latest"
        "react@latest"
        "react-dom@latest"
        "@monaco-editor/react@^4.6.0"
    )

    # Dev dependencies
    local dev_deps=(
        "typescript@latest"
        "@types/node@latest"
        "@types/react@latest"
        "@types/react-dom@latest"
        "tailwindcss@latest"
        "postcss@latest"
        "autoprefixer@latest"
        "eslint@latest"
        "eslint-config-next@latest"
    )

    while [[ $attempt -le $MAX_RETRIES ]]; do
        log "INFO" "npm install attempt $attempt of $MAX_RETRIES..."

        if cd "$PROJECT_DIR" && \
           npm install ${deps[*]} >> "$LOG_FILE" 2>&1 && \
           npm install --save-dev ${dev_deps[*]} >> "$LOG_FILE" 2>&1; then
            cd - > /dev/null
            log "INFO" "Dependencies installed successfully"
            return 0
        fi

        cd - > /dev/null 2>/dev/null || true

        if [[ $attempt -lt $MAX_RETRIES ]]; then
            log "WARN" "npm install failed, retrying in ${RETRY_BACKOFF}s..."
            sleep "$RETRY_BACKOFF"
        fi
        ((attempt++))
    done

    log "ERROR" "npm install failed after $MAX_RETRIES attempts"
    return 1
}

# ─── Project Structure ────────────────────────────────────────────────────────
create_project_structure() {
    log "INFO" "Creating project structure..."

    local dirs=(
        "app"
        "app/api/health"
        "app/(routes)"
        "components/ui"
        "components/layout"
        "components/shared"
        "hooks"
        "lib"
        "public"
        "styles"
        "types"
    )

    for dir in "${dirs[@]}"; do
        mkdir -p "$PROJECT_DIR/src/$dir"
    done

    # Root-level app layout
    cat > "$PROJECT_DIR/src/app/layout.tsx" << 'LAYOUT'
import type { Metadata } from "next";
import "@/styles/globals.css";
import { ToastProvider } from "@/components/ui/ToastProvider";

export const metadata: Metadata = {
  title: "Frontend App",
  description: "Production-grade Next.js application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        <ToastProvider>{children}</ToastProvider>
      </body>
    </html>
  );
}
LAYOUT

    # Root page
    cat > "$PROJECT_DIR/src/app/page.tsx" << 'PAGE'
import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold mb-4">Frontend App</h1>
      <p className="text-gray-600 mb-8">Production-grade Next.js application</p>
      <div className="flex gap-4">
        <Link
          href="/dashboard"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Dashboard
        </Link>
      </div>
    </main>
  );
}
PAGE

    # Global styles
    cat > "$PROJECT_DIR/src/styles/globals.css" << 'CSS'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --color-primary: 59 130 246;
    --color-secondary: 107 114 128;
    --color-success: 34 197 94;
    --color-warning: 234 179 8;
    --color-danger: 239 68 68;
    --color-surface: 255 255 255;
    --color-background: 249 250 251;
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --color-surface: 31 41 55;
      --color-background: 17 24 39;
    }
  }
}

@layer components {
  .skeleton {
    @apply animate-pulse bg-gray-200 rounded;
  }

  .skeleton-text {
    @apply skeleton h-4 w-full;
  }

  .skeleton-heading {
    @apply skeleton h-8 w-3/4;
  }

  .skeleton-avatar {
    @apply skeleton h-10 w-10 rounded-full;
  }
}
CSS

    # TypeScript path aliases
    cat > "$PROJECT_DIR/src/types/index.ts" << 'TYPES'
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface ApiError {
  message: string;
  code: string;
  status: number;
  details?: Record<string, string[]>;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface ToastMessage {
  id: string;
  type: "success" | "error" | "warning" | "info";
  message: string;
  duration?: number;
}
TYPES

    log "INFO" "Project structure created"
}

# ─── Configuration Files ─────────────────────────────────────────────────────
create_config_files() {
    log "INFO" "Creating configuration files..."

    # tsconfig.json
    cat > "$PROJECT_DIR/tsconfig.json" << 'TSCONFIG'
{
  "compilerOptions": {
    "target": "es2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
TSCONFIG

    # next.config.js
    cat > "$PROJECT_DIR/next.config.js" << 'NEXTCONFIG'
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  poweredByHeader: false,
  compress: true,

  images: {
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60,
    remotePatterns: [],
  },

  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'X-DNS-Prefetch-Control', value: 'on' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
        ],
      },
      {
        source: '/_next/static/:path*',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
        ],
      },
    ];
  },

  webpack: (config, { isServer }) => {
    // Monaco editor support
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        path: false,
      };
    }
    return config;
  },
};

module.exports = nextConfig;
NEXTCONFIG

    # tailwind.config.ts
    cat > "$PROJECT_DIR/tailwind.config.ts" << 'TAILWIND'
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "rgb(var(--color-primary) / <alpha-value>)",
        secondary: "rgb(var(--color-secondary) / <alpha-value>)",
        success: "rgb(var(--color-success) / <alpha-value>)",
        warning: "rgb(var(--color-warning) / <alpha-value>)",
        danger: "rgb(var(--color-danger) / <alpha-value>)",
        surface: "rgb(var(--color-surface) / <alpha-value>)",
      },
      animation: {
        "fade-in": "fadeIn 0.3s ease-in-out",
        "slide-in-right": "slideInRight 0.3s ease-out",
        "slide-in-up": "slideInUp 0.2s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideInRight: {
          "0%": { transform: "translateX(100%)", opacity: "0" },
          "100%": { transform: "translateX(0)", opacity: "1" },
        },
        slideInUp: {
          "0%": { transform: "translateY(10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
TAILWIND

    # postcss.config.js
    cat > "$PROJECT_DIR/postcss.config.js" << 'POSTCSS'
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
POSTCSS

    # .eslintrc.json
    cat > "$PROJECT_DIR/.eslintrc.json" << 'ESLINT'
{
  "extends": "next/core-web-vitals"
}
ESLINT

    # .gitignore
    cat > "$PROJECT_DIR/.gitignore" << 'GITIGNORE'
# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*

# local env files
.env*.local
.env

# typescript
*.tsbuildinfo
next-env.d.ts
GITIGNORE

    # .dockerignore
    cat > "$PROJECT_DIR/.dockerignore" << 'DOCKERIGNORE'
node_modules
.next
.git
*.md
.env*
docker-compose*.yml
Dockerfile*
.dockerignore
.gitignore
DOCKERIGNORE

    log "INFO" "Configuration files created"
}

# ─── Health Endpoint ──────────────────────────────────────────────────────────
create_health_endpoint() {
    log "INFO" "Creating health check endpoint..."

    cat > "$PROJECT_DIR/src/app/api/health/route.ts" << 'HEALTH'
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || "unknown",
    uptime: process.uptime(),
    environment: process.env.NODE_ENV || "unknown",
  });
}
HEALTH

    log "INFO" "Health endpoint created at /api/health"
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
    log "INFO" "=== Next.js Project Initialization ==="
    log "INFO" "Project: $PROJECT_NAME | Dir: $PROJECT_DIR"

    # Validate prerequisites
    validate_prerequisites || exit $?

    # Check idempotency
    if check_existing_project; then
        exit 0
    fi

    # Create project
    create_project

    echo "[OK] Next.js project initialized ($PROJECT_DIR)"
}

main "$@"
