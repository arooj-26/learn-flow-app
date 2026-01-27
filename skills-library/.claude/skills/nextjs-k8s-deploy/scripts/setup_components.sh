#!/usr/bin/env bash
#
# Setup Production Components
#
# Generates production-grade React components:
# - ErrorBoundary with recovery UI
# - LoadingSkeleton with variants
# - MonacoEditor wrapper (SSR-safe)
# - ResponsiveLayout with breakpoints
# - ApiClient with retry logic
# - ToastProvider notification system
#
# Usage:
#   bash scripts/setup_components.sh
#   PROJECT_DIR=./myapp bash scripts/setup_components.sh
#
# Exit Codes:
#   0 - Success
#   1 - Fatal error
#   2 - Prerequisites not met

set -euo pipefail

# ─── Configuration ────────────────────────────────────────────────────────────
PROJECT_NAME="${PROJECT_NAME:-frontend-app}"
PROJECT_DIR="${PROJECT_DIR:-./${PROJECT_NAME}}"
DEBUG="${DEBUG:-0}"

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
        log "ERROR" "setup_components.sh failed with exit code $exit_code"
        echo -e "${RED}[ERROR]${NC} Component setup failed. Check $LOG_FILE" >&2
    fi
}
trap cleanup EXIT

# ─── Validation ───────────────────────────────────────────────────────────────
validate() {
    if [[ ! -d "$PROJECT_DIR/src" ]]; then
        log "ERROR" "Project directory not found: $PROJECT_DIR/src"
        log "ERROR" "Run init_nextjs.sh first"
        echo "[ERROR] Run init_nextjs.sh first" >&2
        exit 2
    fi
}

# ─── Component: ErrorBoundary ────────────────────────────────────────────────
create_error_boundary() {
    log "INFO" "Creating ErrorBoundary component..."
    local dir="$PROJECT_DIR/src/components/shared"
    mkdir -p "$dir"

    cat > "$dir/ErrorBoundary.tsx" << 'COMPONENT'
"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode);
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  onReset?: () => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error("[ErrorBoundary]", error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  resetErrorBoundary = (): void => {
    this.props.onReset?.();
    this.setState({ hasError: false, error: null });
  };

  render(): ReactNode {
    if (this.state.hasError && this.state.error) {
      if (this.props.fallback) {
        if (typeof this.props.fallback === "function") {
          return this.props.fallback(this.state.error, this.resetErrorBoundary);
        }
        return this.props.fallback;
      }

      return (
        <div className="flex flex-col items-center justify-center min-h-[200px] p-8 bg-red-50 border border-red-200 rounded-lg">
          <svg className="w-12 h-12 text-red-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <h3 className="text-lg font-semibold text-red-800 mb-2">Something went wrong</h3>
          <p className="text-red-600 text-sm mb-4 text-center max-w-md">
            {this.state.error.message || "An unexpected error occurred"}
          </p>
          <button
            onClick={this.resetErrorBoundary}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors text-sm font-medium"
          >
            Try Again
          </button>
          {process.env.NODE_ENV === "development" && (
            <details className="mt-4 w-full max-w-lg">
              <summary className="text-xs text-red-500 cursor-pointer">Stack Trace</summary>
              <pre className="mt-2 text-xs text-red-400 overflow-auto p-2 bg-red-100 rounded max-h-40">
                {this.state.error.stack}
              </pre>
            </details>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
COMPONENT
    log "INFO" "ErrorBoundary created"
}

# ─── Component: LoadingSkeleton ───────────────────────────────────────────────
create_loading_skeleton() {
    log "INFO" "Creating LoadingSkeleton component..."
    local dir="$PROJECT_DIR/src/components/ui"
    mkdir -p "$dir"

    cat > "$dir/LoadingSkeleton.tsx" << 'COMPONENT'
import React from "react";

type SkeletonVariant = "text" | "card" | "table" | "avatar" | "editor";

interface LoadingSkeletonProps {
  variant?: SkeletonVariant;
  lines?: number;
  count?: number;
  className?: string;
}

function SkeletonLine({ width = "100%" }: { width?: string }) {
  return (
    <div
      className="skeleton-text mb-2"
      style={{ width }}
    />
  );
}

function TextSkeleton({ lines = 3 }: { lines: number }) {
  const widths = ["100%", "92%", "78%", "85%", "60%"];
  return (
    <div className="space-y-2">
      {Array.from({ length: lines }, (_, i) => (
        <SkeletonLine key={i} width={widths[i % widths.length]} />
      ))}
    </div>
  );
}

function CardSkeleton() {
  return (
    <div className="border border-gray-200 rounded-lg p-4 space-y-3">
      <div className="skeleton h-6 w-2/3" />
      <div className="skeleton-text w-full" />
      <div className="skeleton-text w-4/5" />
      <div className="flex gap-2 mt-4">
        <div className="skeleton h-8 w-20 rounded-md" />
        <div className="skeleton h-8 w-20 rounded-md" />
      </div>
    </div>
  );
}

function TableSkeleton() {
  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <div className="bg-gray-100 p-3 flex gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="skeleton h-4 flex-1" />
        ))}
      </div>
      {[...Array(5)].map((_, row) => (
        <div key={row} className="p-3 flex gap-4 border-t border-gray-100">
          {[...Array(4)].map((_, col) => (
            <div key={col} className="skeleton h-4 flex-1" />
          ))}
        </div>
      ))}
    </div>
  );
}

function AvatarSkeleton() {
  return (
    <div className="flex items-center gap-3">
      <div className="skeleton-avatar" />
      <div className="space-y-2 flex-1">
        <div className="skeleton h-4 w-1/3" />
        <div className="skeleton h-3 w-1/2" />
      </div>
    </div>
  );
}

function EditorSkeleton() {
  const lineWidths = ["70%", "45%", "85%", "60%", "30%", "90%", "55%", "75%", "40%", "65%"];
  return (
    <div className="bg-gray-900 rounded-lg p-4 font-mono space-y-1.5">
      {lineWidths.map((width, i) => (
        <div key={i} className="flex gap-3 items-center">
          <span className="text-gray-600 text-xs w-6 text-right">{i + 1}</span>
          <div
            className="h-3.5 rounded-sm animate-pulse"
            style={{
              width,
              backgroundColor: i % 3 === 0 ? "#374151" : i % 3 === 1 ? "#1f2937" : "#4b5563",
            }}
          />
        </div>
      ))}
    </div>
  );
}

export function LoadingSkeleton({
  variant = "text",
  lines = 3,
  count = 1,
  className = "",
}: LoadingSkeletonProps) {
  const renderVariant = () => {
    switch (variant) {
      case "text":
        return <TextSkeleton lines={lines} />;
      case "card":
        return <CardSkeleton />;
      case "table":
        return <TableSkeleton />;
      case "avatar":
        return <AvatarSkeleton />;
      case "editor":
        return <EditorSkeleton />;
      default:
        return <TextSkeleton lines={lines} />;
    }
  };

  return (
    <div className={`animate-fade-in ${className}`} role="status" aria-label="Loading">
      {Array.from({ length: count }, (_, i) => (
        <div key={i} className={i > 0 ? "mt-4" : ""}>
          {renderVariant()}
        </div>
      ))}
      <span className="sr-only">Loading...</span>
    </div>
  );
}

export default LoadingSkeleton;
COMPONENT
    log "INFO" "LoadingSkeleton created"
}

# ─── Component: MonacoEditor ─────────────────────────────────────────────────
create_monaco_editor() {
    log "INFO" "Creating MonacoEditor component..."
    local dir="$PROJECT_DIR/src/components/shared"
    mkdir -p "$dir"

    cat > "$dir/MonacoEditor.tsx" << 'COMPONENT'
"use client";

import React, { useCallback, useRef } from "react";
import dynamic from "next/dynamic";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";

const Editor = dynamic(() => import("@monaco-editor/react"), {
  ssr: false,
  loading: () => <LoadingSkeleton variant="editor" />,
});

interface MonacoEditorProps {
  value: string;
  language?: string;
  theme?: "vs-dark" | "vs-light" | "hc-black";
  height?: string | number;
  readOnly?: boolean;
  onChange?: (value: string) => void;
  onSave?: (value: string) => void;
  onMount?: (editor: unknown, monaco: unknown) => void;
  options?: Record<string, unknown>;
  loading?: React.ReactNode;
  className?: string;
}

const LANGUAGE_MAP: Record<string, string> = {
  js: "javascript",
  ts: "typescript",
  py: "python",
  yml: "yaml",
  md: "markdown",
  sh: "shell",
  bash: "shell",
  dockerfile: "dockerfile",
};

function resolveLanguage(lang?: string, filename?: string): string {
  if (lang) return LANGUAGE_MAP[lang] || lang;
  if (filename) {
    const ext = filename.split(".").pop()?.toLowerCase() || "";
    return LANGUAGE_MAP[ext] || ext;
  }
  return "plaintext";
}

export function MonacoEditorWrapper({
  value,
  language = "typescript",
  theme = "vs-dark",
  height = "400px",
  readOnly = false,
  onChange,
  onSave,
  onMount,
  options = {},
  loading,
  className = "",
}: MonacoEditorProps) {
  const editorRef = useRef<unknown>(null);

  const handleMount = useCallback(
    (editor: unknown, monaco: unknown) => {
      editorRef.current = editor;

      // Register Ctrl+S / Cmd+S handler
      if (onSave && editor && typeof (editor as any).addCommand === "function") {
        (editor as any).addCommand(
          (monaco as any).KeyMod.CtrlCmd | (monaco as any).KeyCode.KeyS,
          () => {
            const currentValue = (editor as any).getValue();
            onSave(currentValue);
          }
        );
      }

      onMount?.(editor, monaco);
    },
    [onSave, onMount]
  );

  const handleChange = useCallback(
    (val: string | undefined) => {
      if (val !== undefined) {
        onChange?.(val);
      }
    },
    [onChange]
  );

  const resolvedLanguage = resolveLanguage(language);

  return (
    <div className={`border border-gray-700 rounded-lg overflow-hidden ${className}`}>
      <div className="bg-gray-800 px-3 py-1.5 flex items-center justify-between border-b border-gray-700">
        <span className="text-xs text-gray-400 font-mono">{resolvedLanguage}</span>
        <div className="flex items-center gap-2">
          {readOnly && (
            <span className="text-xs text-gray-500 bg-gray-700 px-2 py-0.5 rounded">
              Read Only
            </span>
          )}
        </div>
      </div>
      <Editor
        height={height}
        language={resolvedLanguage}
        theme={theme}
        value={value}
        onChange={handleChange}
        onMount={handleMount}
        loading={loading || <LoadingSkeleton variant="editor" />}
        options={{
          readOnly,
          minimap: { enabled: false },
          wordWrap: "on",
          fontSize: 14,
          lineNumbers: "on",
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 2,
          padding: { top: 8 },
          ...options,
        }}
      />
    </div>
  );
}

export default MonacoEditorWrapper;
COMPONENT
    log "INFO" "MonacoEditor created"
}

# ─── Component: ResponsiveLayout ─────────────────────────────────────────────
create_responsive_layout() {
    log "INFO" "Creating ResponsiveLayout component..."
    local dir="$PROJECT_DIR/src/components/layout"
    mkdir -p "$dir"

    cat > "$dir/ResponsiveLayout.tsx" << 'COMPONENT'
"use client";

import React, { useState, useCallback, useEffect, ReactNode } from "react";

interface ResponsiveLayoutProps {
  children: ReactNode;
  sidebar?: ReactNode;
  navbar?: ReactNode;
  footer?: ReactNode;
  mode?: "sidebar" | "topnav" | "minimal";
  sidebarCollapsed?: boolean;
  onSidebarToggle?: (collapsed: boolean) => void;
}

function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);
  useEffect(() => {
    if (typeof window === "undefined") return;
    const mql = window.matchMedia(query);
    setMatches(mql.matches);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, [query]);
  return matches;
}

export function ResponsiveLayout({
  children,
  sidebar,
  navbar,
  footer,
  mode = "sidebar",
  sidebarCollapsed: controlledCollapsed,
  onSidebarToggle,
}: ResponsiveLayoutProps) {
  const isMobile = useMediaQuery("(max-width: 767px)");
  const isTablet = useMediaQuery("(min-width: 768px) and (max-width: 1023px)");
  const [internalCollapsed, setInternalCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const collapsed = controlledCollapsed ?? internalCollapsed;

  const toggleSidebar = useCallback(() => {
    if (isMobile) {
      setMobileOpen((prev) => !prev);
    } else {
      const newState = !collapsed;
      setInternalCollapsed(newState);
      onSidebarToggle?.(newState);
    }
  }, [isMobile, collapsed, onSidebarToggle]);

  // Auto-collapse on tablet
  useEffect(() => {
    if (isTablet && !controlledCollapsed) {
      setInternalCollapsed(true);
    }
  }, [isTablet, controlledCollapsed]);

  // Close mobile drawer on resize
  useEffect(() => {
    if (!isMobile) setMobileOpen(false);
  }, [isMobile]);

  if (mode === "minimal") {
    return (
      <div className="min-h-screen flex flex-col">
        {navbar}
        <main className="flex-1 p-4 md:p-6 lg:p-8">{children}</main>
        {footer}
      </div>
    );
  }

  if (mode === "topnav") {
    return (
      <div className="min-h-screen flex flex-col">
        <header className="sticky top-0 z-40 h-16 border-b border-gray-200 bg-white shadow-sm">
          {navbar}
        </header>
        <main className="flex-1 p-4 md:p-6 lg:p-8">{children}</main>
        {footer}
      </div>
    );
  }

  // Sidebar mode
  const sidebarWidth = collapsed ? "w-16" : "w-[280px]";

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top navbar */}
      <header className="sticky top-0 z-40 h-14 border-b border-gray-200 bg-white shadow-sm flex items-center px-4">
        <button
          onClick={toggleSidebar}
          className="p-2 rounded-md hover:bg-gray-100 transition-colors mr-3"
          aria-label="Toggle sidebar"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <div className="flex-1">{navbar}</div>
      </header>

      <div className="flex flex-1">
        {/* Mobile overlay */}
        {isMobile && mobileOpen && (
          <div
            className="fixed inset-0 z-30 bg-black/50 transition-opacity"
            onClick={() => setMobileOpen(false)}
          />
        )}

        {/* Sidebar */}
        {sidebar && (
          <aside
            className={`
              ${isMobile
                ? `fixed top-14 left-0 z-40 h-[calc(100vh-3.5rem)] w-[280px] transform transition-transform duration-200 ${mobileOpen ? "translate-x-0" : "-translate-x-full"}`
                : `sticky top-14 h-[calc(100vh-3.5rem)] ${sidebarWidth} transition-all duration-200`
              }
              bg-white border-r border-gray-200 overflow-y-auto
            `}
          >
            {sidebar}
          </aside>
        )}

        {/* Main content */}
        <main className="flex-1 min-w-0 p-4 md:p-6 lg:p-8 overflow-auto">
          {children}
        </main>
      </div>

      {footer && (
        <footer className="border-t border-gray-200 bg-white p-4">
          {footer}
        </footer>
      )}
    </div>
  );
}

export default ResponsiveLayout;
COMPONENT
    log "INFO" "ResponsiveLayout created"
}

# ─── Component: ApiClient ─────────────────────────────────────────────────────
create_api_client() {
    log "INFO" "Creating ApiClient..."
    local dir="$PROJECT_DIR/src/lib"
    mkdir -p "$dir"

    cat > "$dir/api-client.ts" << 'COMPONENT'
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "/api";
const DEFAULT_TIMEOUT = 30000;
const DEFAULT_RETRIES = 3;
const DEFAULT_RETRY_DELAY = 1000;

// ─── Error Types ─────────────────────────────────────────────────────────────

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code: string,
    public details?: Record<string, string[]>
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export class NetworkError extends ApiError {
  constructor(message = "Network error") {
    super(message, 0, "NETWORK_ERROR");
    this.name = "NetworkError";
  }
}

export class TimeoutError extends ApiError {
  constructor(message = "Request timed out") {
    super(message, 0, "TIMEOUT");
    this.name = "TimeoutError";
  }
}

export class AuthError extends ApiError {
  constructor(message = "Unauthorized", status = 401) {
    super(message, status, "AUTH_ERROR");
    this.name = "AuthError";
  }
}

export class ValidationError extends ApiError {
  constructor(message: string, details?: Record<string, string[]>) {
    super(message, 422, "VALIDATION_ERROR", details);
    this.name = "ValidationError";
  }
}

// ─── Response Mapping ────────────────────────────────────────────────────────

function mapResponseError(status: number, body: Record<string, unknown>): ApiError {
  const message = (body.message as string) || (body.detail as string) || "Request failed";

  switch (status) {
    case 401:
    case 403:
      return new AuthError(message, status);
    case 404:
      return new ApiError(message, 404, "NOT_FOUND");
    case 422:
      return new ValidationError(message, body.errors as Record<string, string[]>);
    default:
      if (status >= 500) {
        return new ApiError(message, status, "SERVER_ERROR");
      }
      return new ApiError(message, status, "REQUEST_ERROR");
  }
}

// ─── Retry Logic ─────────────────────────────────────────────────────────────

const RETRYABLE_STATUSES = new Set([502, 503, 504]);

function isRetryable(error: unknown): boolean {
  if (error instanceof NetworkError || error instanceof TimeoutError) return true;
  if (error instanceof ApiError && RETRYABLE_STATUSES.has(error.status)) return true;
  return false;
}

async function withRetry<T>(
  fn: () => Promise<T>,
  retries: number,
  delay: number
): Promise<T> {
  let lastError: unknown;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (attempt < retries && isRetryable(error)) {
        const backoff = delay * Math.pow(2, attempt);
        await new Promise((resolve) => setTimeout(resolve, backoff));
        continue;
      }
      throw error;
    }
  }

  throw lastError;
}

// ─── Fetch with Timeout ──────────────────────────────────────────────────────

async function fetchWithTimeout(
  url: string,
  options: RequestInit,
  timeout: number
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    return response;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new TimeoutError();
    }
    throw new NetworkError(
      error instanceof Error ? error.message : "Network error"
    );
  } finally {
    clearTimeout(timeoutId);
  }
}

// ─── API Client ──────────────────────────────────────────────────────────────

interface RequestOptions {
  headers?: Record<string, string>;
  timeout?: number;
  retries?: number;
  retryDelay?: number;
  params?: Record<string, string | number | boolean>;
}

class ApiClient {
  private baseURL: string;
  private defaultHeaders: Record<string, string>;
  private defaultTimeout: number;
  private defaultRetries: number;
  private defaultRetryDelay: number;

  constructor(config?: {
    baseURL?: string;
    headers?: Record<string, string>;
    timeout?: number;
    retries?: number;
    retryDelay?: number;
  }) {
    this.baseURL = config?.baseURL || API_BASE_URL;
    this.defaultHeaders = {
      "Content-Type": "application/json",
      ...config?.headers,
    };
    this.defaultTimeout = config?.timeout || DEFAULT_TIMEOUT;
    this.defaultRetries = config?.retries || DEFAULT_RETRIES;
    this.defaultRetryDelay = config?.retryDelay || DEFAULT_RETRY_DELAY;
  }

  private buildURL(path: string, params?: Record<string, string | number | boolean>): string {
    const url = `${this.baseURL}${path.startsWith("/") ? path : `/${path}`}`;
    if (!params) return url;

    const searchParams = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
      searchParams.set(key, String(value));
    }
    return `${url}?${searchParams.toString()}`;
  }

  private async request<T>(
    method: string,
    path: string,
    body?: unknown,
    options?: RequestOptions
  ): Promise<T> {
    const url = this.buildURL(path, options?.params);
    const timeout = options?.timeout || this.defaultTimeout;
    const retries = options?.retries ?? this.defaultRetries;
    const retryDelay = options?.retryDelay || this.defaultRetryDelay;

    const headers: Record<string, string> = {
      ...this.defaultHeaders,
      ...options?.headers,
    };

    const fetchOptions: RequestInit = {
      method,
      headers,
      ...(body ? { body: JSON.stringify(body) } : {}),
    };

    return withRetry(
      async () => {
        const response = await fetchWithTimeout(url, fetchOptions, timeout);

        if (!response.ok) {
          let errorBody: Record<string, unknown> = {};
          try {
            errorBody = await response.json();
          } catch {
            // Response body not JSON
          }
          throw mapResponseError(response.status, errorBody);
        }

        if (response.status === 204) {
          return undefined as T;
        }

        return response.json() as Promise<T>;
      },
      retries,
      retryDelay
    );
  }

  async get<T>(path: string, options?: RequestOptions): Promise<T> {
    return this.request<T>("GET", path, undefined, options);
  }

  async post<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return this.request<T>("POST", path, body, options);
  }

  async put<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return this.request<T>("PUT", path, body, options);
  }

  async patch<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return this.request<T>("PATCH", path, body, options);
  }

  async delete<T>(path: string, options?: RequestOptions): Promise<T> {
    return this.request<T>("DELETE", path, undefined, options);
  }

  async upload<T>(path: string, formData: FormData, options?: RequestOptions): Promise<T> {
    const url = this.buildURL(path, options?.params);
    const timeout = options?.timeout || this.defaultTimeout;

    // Remove Content-Type so browser sets multipart boundary
    const headers = { ...this.defaultHeaders, ...options?.headers };
    delete headers["Content-Type"];

    const response = await fetchWithTimeout(
      url,
      { method: "POST", headers, body: formData },
      timeout
    );

    if (!response.ok) {
      let errorBody: Record<string, unknown> = {};
      try {
        errorBody = await response.json();
      } catch {}
      throw mapResponseError(response.status, errorBody);
    }

    return response.json() as Promise<T>;
  }
}

// Singleton instance
export const apiClient = new ApiClient();

export default ApiClient;
COMPONENT
    log "INFO" "ApiClient created"
}

# ─── Component: ToastProvider ─────────────────────────────────────────────────
create_toast_provider() {
    log "INFO" "Creating ToastProvider component..."
    local dir="$PROJECT_DIR/src/components/ui"
    mkdir -p "$dir"

    cat > "$dir/ToastProvider.tsx" << 'COMPONENT'
"use client";

import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  ReactNode,
} from "react";
import { createPortal } from "react-dom";

// ─── Types ───────────────────────────────────────────────────────────────────

type ToastType = "success" | "error" | "warning" | "info";

interface Toast {
  id: string;
  type: ToastType;
  message: string;
  duration: number;
  pausedAt?: number;
}

interface ToastOptions {
  duration?: number;
}

interface ToastContextValue {
  toast: {
    success: (message: string, options?: ToastOptions) => string;
    error: (message: string, options?: ToastOptions) => string;
    warning: (message: string, options?: ToastOptions) => string;
    info: (message: string, options?: ToastOptions) => string;
    dismiss: (id?: string) => void;
  };
}

// ─── Context ─────────────────────────────────────────────────────────────────

const ToastContext = createContext<ToastContextValue | null>(null);

export function useToast(): ToastContextValue {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return context;
}

// ─── Icons ───────────────────────────────────────────────────────────────────

const ICONS: Record<ToastType, ReactNode> = {
  success: (
    <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
    </svg>
  ),
  error: (
    <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
    </svg>
  ),
  warning: (
    <svg className="w-5 h-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
    </svg>
  ),
  info: (
    <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
};

const BORDER_COLORS: Record<ToastType, string> = {
  success: "border-l-green-500",
  error: "border-l-red-500",
  warning: "border-l-yellow-500",
  info: "border-l-blue-500",
};

// ─── Toast Item ──────────────────────────────────────────────────────────────

function ToastItem({
  toast,
  onDismiss,
  onPause,
  onResume,
}: {
  toast: Toast;
  onDismiss: (id: string) => void;
  onPause: (id: string) => void;
  onResume: (id: string) => void;
}) {
  return (
    <div
      role="alert"
      aria-live="polite"
      className={`
        flex items-start gap-3 p-4 bg-white rounded-lg shadow-lg border border-gray-200
        border-l-4 ${BORDER_COLORS[toast.type]}
        animate-slide-in-right
        max-w-sm w-full
      `}
      onMouseEnter={() => onPause(toast.id)}
      onMouseLeave={() => onResume(toast.id)}
    >
      <span className="flex-shrink-0 mt-0.5">{ICONS[toast.type]}</span>
      <p className="text-sm text-gray-700 flex-1">{toast.message}</p>
      <button
        onClick={() => onDismiss(toast.id)}
        className="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
        aria-label="Dismiss"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );
}

// ─── Provider ────────────────────────────────────────────────────────────────

interface ToastProviderProps {
  children: ReactNode;
  position?: "top-right" | "top-left" | "bottom-right" | "bottom-left";
  maxToasts?: number;
  defaultDuration?: number;
}

export function ToastProvider({
  children,
  position = "top-right",
  maxToasts = 5,
  defaultDuration = 5000,
}: ToastProviderProps) {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Auto-dismiss timers
  useEffect(() => {
    const timers = toasts
      .filter((t) => !t.pausedAt)
      .map((t) =>
        setTimeout(() => {
          setToasts((prev) => prev.filter((toast) => toast.id !== t.id));
        }, t.duration)
      );

    return () => timers.forEach(clearTimeout);
  }, [toasts]);

  const addToast = useCallback(
    (type: ToastType, message: string, options?: ToastOptions): string => {
      const id = `toast-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
      const duration = options?.duration || defaultDuration;

      setToasts((prev) => {
        const next = [...prev, { id, type, message, duration }];
        return next.length > maxToasts ? next.slice(-maxToasts) : next;
      });

      return id;
    },
    [defaultDuration, maxToasts]
  );

  const dismiss = useCallback((id?: string) => {
    if (id) {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    } else {
      setToasts([]);
    }
  }, []);

  const pause = useCallback((id: string) => {
    setToasts((prev) =>
      prev.map((t) => (t.id === id ? { ...t, pausedAt: Date.now() } : t))
    );
  }, []);

  const resume = useCallback((id: string) => {
    setToasts((prev) =>
      prev.map((t) => (t.id === id ? { ...t, pausedAt: undefined } : t))
    );
  }, []);

  const toast = {
    success: (msg: string, opts?: ToastOptions) => addToast("success", msg, opts),
    error: (msg: string, opts?: ToastOptions) => addToast("error", msg, opts),
    warning: (msg: string, opts?: ToastOptions) => addToast("warning", msg, opts),
    info: (msg: string, opts?: ToastOptions) => addToast("info", msg, opts),
    dismiss,
  };

  const positionClasses: Record<string, string> = {
    "top-right": "top-4 right-4",
    "top-left": "top-4 left-4",
    "bottom-right": "bottom-4 right-4",
    "bottom-left": "bottom-4 left-4",
  };

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      {mounted &&
        createPortal(
          <div
            className={`fixed z-50 ${positionClasses[position]} flex flex-col gap-2`}
            aria-live="polite"
            aria-label="Notifications"
          >
            {toasts.map((t) => (
              <ToastItem
                key={t.id}
                toast={t}
                onDismiss={dismiss}
                onPause={pause}
                onResume={resume}
              />
            ))}
          </div>,
          document.body
        )}
    </ToastContext.Provider>
  );
}

export default ToastProvider;
COMPONENT
    log "INFO" "ToastProvider created"
}

# ─── useApi Hook ──────────────────────────────────────────────────────────────
create_use_api_hook() {
    log "INFO" "Creating useApi hook..."
    local dir="$PROJECT_DIR/src/hooks"
    mkdir -p "$dir"

    cat > "$dir/useApi.ts" << 'COMPONENT'
"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { apiClient, ApiError } from "@/lib/api-client";

interface UseApiOptions {
  enabled?: boolean;
  refetchInterval?: number;
  onSuccess?: (data: unknown) => void;
  onError?: (error: ApiError) => void;
}

interface UseApiResult<T> {
  data: T | null;
  error: ApiError | null;
  loading: boolean;
  refetch: () => Promise<void>;
}

export function useApi<T>(path: string, options: UseApiOptions = {}): UseApiResult<T> {
  const { enabled = true, refetchInterval, onSuccess, onError } = options;
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<ApiError | null>(null);
  const [loading, setLoading] = useState(enabled);
  const mountedRef = useRef(true);

  const fetchData = useCallback(async () => {
    if (!mountedRef.current) return;
    setLoading(true);
    setError(null);

    try {
      const result = await apiClient.get<T>(path);
      if (mountedRef.current) {
        setData(result);
        onSuccess?.(result);
      }
    } catch (err) {
      if (mountedRef.current) {
        const apiError = err instanceof ApiError ? err : new ApiError("Unknown error", 0, "UNKNOWN");
        setError(apiError);
        onError?.(apiError);
      }
    } finally {
      if (mountedRef.current) {
        setLoading(false);
      }
    }
  }, [path, onSuccess, onError]);

  useEffect(() => {
    mountedRef.current = true;
    if (enabled) {
      fetchData();
    }
    return () => {
      mountedRef.current = false;
    };
  }, [enabled, fetchData]);

  useEffect(() => {
    if (!refetchInterval || !enabled) return;
    const interval = setInterval(fetchData, refetchInterval);
    return () => clearInterval(interval);
  }, [refetchInterval, enabled, fetchData]);

  return { data, error, loading, refetch: fetchData };
}

export default useApi;
COMPONENT
    log "INFO" "useApi hook created"
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
    log "INFO" "=== Setting Up Production Components ==="
    validate

    local count=0
    create_error_boundary; ((count++))
    create_loading_skeleton; ((count++))
    create_monaco_editor; ((count++))
    create_responsive_layout; ((count++))
    create_api_client; ((count++))
    create_toast_provider; ((count++))
    create_use_api_hook; ((count++))

    echo "[OK] Components generated ($count components)"
}

main "$@"
