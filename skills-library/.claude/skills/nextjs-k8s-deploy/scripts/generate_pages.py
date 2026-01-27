#!/usr/bin/env python3
"""
Generate Next.js Pages

Creates production-grade Next.js App Router pages with:
- Responsive layout integration
- Error boundary wrapping
- Loading states (Suspense + skeleton)
- Monaco editor integration (optional)
- API data fetching patterns
- Breadcrumb navigation

Usage:
    python generate_pages.py --project-dir ./frontend-app --pages dashboard,settings,editor
    python generate_pages.py --project-dir ./frontend-app --pages editor --with-monaco
    python generate_pages.py --project-dir ./frontend-app --pages dashboard --api-base-url /api/v1
    python generate_pages.py --project-dir ./frontend-app --pages dashboard --layout topnav

Options:
    --project-dir   Project root directory (default: ./frontend-app)
    --pages         Comma-separated page names (default: dashboard)
    --with-monaco   Include Monaco editor component on pages
    --api-base-url  Base URL for API connections (default: /api)
    --layout        Layout type: sidebar, topnav, minimal (default: sidebar)

Exit Codes:
    0 - Success
    1 - Fatal error
    2 - Validation error
"""

import argparse
import io
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

# Windows UTF-8 compatibility
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ─── Configuration ────────────────────────────────────────────────────────────

DEBUG = os.environ.get("DEBUG", "0") == "1"
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = os.environ.get("LOG_FILE", str(SCRIPT_DIR.parent / ".nextjs-k8s-deploy.log"))


# ─── Logging ──────────────────────────────────────────────────────────────────

def log(level: str, message: str):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    log_line = f"[{timestamp}] [{level}] {message}"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except OSError:
        pass
    if DEBUG or level == "ERROR":
        out = sys.stderr if level == "ERROR" else sys.stdout
        print(log_line, file=out)


# ─── Validation ───────────────────────────────────────────────────────────────

def validate_inputs(project_dir: str, pages: list[str]) -> tuple[bool, str]:
    if not os.path.isdir(project_dir):
        return False, f"Project directory not found: {project_dir}"
    src_dir = os.path.join(project_dir, "src")
    if not os.path.isdir(src_dir):
        return False, f"src/ directory not found in {project_dir}. Run init_nextjs.sh first."
    for page in pages:
        if not page.isidentifier() and not page.replace("-", "_").isidentifier():
            return False, f"Invalid page name: '{page}'. Use alphanumeric and hyphens only."
    return True, ""


def sanitize_page_name(name: str) -> str:
    """Convert page name to valid identifier for component names."""
    parts = name.replace("_", "-").split("-")
    return "".join(p.capitalize() for p in parts)


# ─── Page Templates ──────────────────────────────────────────────────────────

def generate_page_tsx(page_name: str, component_name: str, with_monaco: bool, api_base_url: str, layout: str) -> str:
    """Generate the main page.tsx file."""

    monaco_import = ""
    monaco_section = ""
    if with_monaco:
        monaco_import = 'import { MonacoEditorWrapper } from "@/components/shared/MonacoEditor";'
        monaco_section = dedent(f"""\

          {{/* Code Editor Section */}}
          <section className="mt-8">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Code Editor</h2>
            <{component_name}Editor />
          </section>""")

    api_hook_import = ""
    api_data_section = ""
    if api_base_url:
        api_hook_import = 'import { useApi } from "@/hooks/useApi";'
        api_data_section = dedent(f"""\

          {{/* Data Section */}}
          <section className="mt-6">
            <{component_name}Data />
          </section>""")

    layout_import = ""
    layout_wrapper_open = ""
    layout_wrapper_close = ""
    sidebar_content = ""

    if layout in ("sidebar", "topnav"):
        layout_import = 'import {{ ResponsiveLayout }} from "@/components/layout/ResponsiveLayout";'
        sidebar_jsx = ""
        if layout == "sidebar":
            sidebar_jsx = dedent(f"""\
              sidebar={{
                <nav className="p-4 space-y-2">
                  <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider px-2 mb-3">
                    Navigation
                  </h3>
                  <a href="/dashboard" className="block px-3 py-2 rounded-md text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                    Dashboard
                  </a>
                  <a href="/settings" className="block px-3 py-2 rounded-md text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                    Settings
                  </a>
                  <a href="/editor" className="block px-3 py-2 rounded-md text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                    Editor
                  </a>
                </nav>
              }}""")

        layout_wrapper_open = dedent(f"""\
    <ResponsiveLayout
          mode="{layout}"
          {sidebar_jsx}
          navbar={{
            <div className="flex items-center justify-between w-full">
              <span className="font-semibold text-gray-800">Frontend App</span>
              <span className="text-sm text-gray-500">v0.1.0</span>
            </div>
          }}
        >""")
        layout_wrapper_close = "    </ResponsiveLayout>"

    return dedent(f"""\
        import {{ Suspense }} from "react";
        import {{ ErrorBoundary }} from "@/components/shared/ErrorBoundary";
        import {{ LoadingSkeleton }} from "@/components/ui/LoadingSkeleton";
        {layout_import}
        {monaco_import}
        {api_hook_import}
        import {component_name}Content from "./{component_name}Content";
        {"import " + component_name + "Editor from './" + component_name + "Editor';" if with_monaco else ""}
        {"import " + component_name + "Data from './" + component_name + "Data';" if api_base_url else ""}

        export const metadata = {{
          title: "{component_name} | Frontend App",
          description: "{component_name} page",
        }};

        export default function {component_name}Page() {{
          return (
        {layout_wrapper_open or "    <>"}
              <div className="max-w-7xl mx-auto">
                {{/* Breadcrumb */}}
                <nav className="mb-4 text-sm text-gray-500" aria-label="Breadcrumb">
                  <ol className="flex items-center gap-1">
                    <li><a href="/" className="hover:text-gray-700 transition-colors">Home</a></li>
                    <li>/</li>
                    <li className="text-gray-900 font-medium">{component_name}</li>
                  </ol>
                </nav>

                {{/* Page Header */}}
                <header className="mb-6">
                  <h1 className="text-2xl font-bold text-gray-900">{component_name}</h1>
                  <p className="text-gray-500 mt-1">Manage your {page_name.replace("-", " ")} settings and data.</p>
                </header>

                {{/* Main Content with Error Boundary */}}
                <ErrorBoundary>
                  <Suspense fallback={{<LoadingSkeleton variant="card" count={{3}} />}}>
                    <{component_name}Content />
                  </Suspense>
                </ErrorBoundary>
                {api_data_section}
                {monaco_section}
              </div>
        {layout_wrapper_close or "    </>"}
          );
        }}
    """)


def generate_content_component(component_name: str, page_name: str) -> str:
    """Generate the main content component for a page."""
    return dedent(f"""\
        "use client";

        import React from "react";

        export default function {component_name}Content() {{
          return (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {{/* Stats Cards */}}
              <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-gray-500">Total Items</h3>
                  <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={{2}} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                  </svg>
                </div>
                <p className="text-3xl font-bold text-gray-900">--</p>
                <p className="text-xs text-gray-400 mt-1">Updated just now</p>
              </div>

              <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-gray-500">Active</h3>
                  <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={{2}} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <p className="text-3xl font-bold text-gray-900">--</p>
                <p className="text-xs text-gray-400 mt-1">Updated just now</p>
              </div>

              <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-gray-500">Errors</h3>
                  <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={{2}} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <p className="text-3xl font-bold text-gray-900">--</p>
                <p className="text-xs text-gray-400 mt-1">Updated just now</p>
              </div>

              {{/* Content Area */}}
              <div className="col-span-1 md:col-span-2 lg:col-span-3 bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                <h2 className="text-lg font-semibold text-gray-800 mb-4">{component_name} Overview</h2>
                <p className="text-gray-600">
                  This is the {page_name.replace("-", " ")} page. Connect your API data source to populate this view.
                </p>
              </div>
            </div>
          );
        }}
    """)


def generate_editor_component(component_name: str) -> str:
    """Generate Monaco editor wrapper for a page."""
    return dedent(f"""\
        "use client";

        import React, {{ useState, useCallback }} from "react";
        import {{ MonacoEditorWrapper }} from "@/components/shared/MonacoEditor";
        import {{ useToast }} from "@/components/ui/ToastProvider";

        const DEFAULT_CODE = `// {component_name} Editor
        // Write your code here

        interface Config {{
          apiUrl: string;
          timeout: number;
          retries: number;
        }}

        const config: Config = {{
          apiUrl: process.env.NEXT_PUBLIC_API_URL || "/api",
          timeout: 30000,
          retries: 3,
        }};

        export default config;
        `;

        export default function {component_name}Editor() {{
          const [code, setCode] = useState(DEFAULT_CODE);
          const {{ toast }} = useToast();

          const handleSave = useCallback(
            (value: string) => {{
              setCode(value);
              toast.success("Code saved successfully");
            }},
            [toast]
          );

          return (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-500">
                  Press <kbd className="px-1.5 py-0.5 bg-gray-100 border border-gray-300 rounded text-xs font-mono">Ctrl+S</kbd> to save
                </p>
                <span className="text-xs text-gray-400">TypeScript</span>
              </div>
              <MonacoEditorWrapper
                value={{code}}
                language="typescript"
                theme="vs-dark"
                height="400px"
                onChange={{setCode}}
                onSave={{handleSave}}
              />
            </div>
          );
        }}
    """)


def generate_data_component(component_name: str, api_base_url: str) -> str:
    """Generate API data fetching component."""
    return dedent(f"""\
        "use client";

        import React from "react";
        import {{ useApi }} from "@/hooks/useApi";
        import {{ LoadingSkeleton }} from "@/components/ui/LoadingSkeleton";
        import {{ ErrorBoundary }} from "@/components/shared/ErrorBoundary";

        interface DataItem {{
          id: string;
          name: string;
          status: string;
          updatedAt: string;
        }}

        interface DataResponse {{
          data: DataItem[];
          total: number;
        }}

        export default function {component_name}Data() {{
          const {{ data, error, loading, refetch }} = useApi<DataResponse>(
            "{api_base_url}/{component_name.lower()}",
            {{ refetchInterval: 30000 }}
          );

          if (loading) {{
            return <LoadingSkeleton variant="table" />;
          }}

          if (error) {{
            return (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={{2}} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-sm font-medium text-red-800">Failed to load data</p>
                </div>
                <p className="text-sm text-red-600">{{error.message}}</p>
                <button
                  onClick={{refetch}}
                  className="mt-3 px-3 py-1.5 text-sm bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
                >
                  Retry
                </button>
              </div>
            );
          }}

          const items = data?.data || [];

          return (
            <ErrorBoundary>
              <div className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm">
                <div className="px-4 py-3 border-b border-gray-200 flex items-center justify-between">
                  <h3 className="text-sm font-semibold text-gray-700">
                    Data ({{data?.total || 0}} items)
                  </h3>
                  <button
                    onClick={{refetch}}
                    className="text-sm text-blue-600 hover:text-blue-800 transition-colors"
                  >
                    Refresh
                  </button>
                </div>

                {{items.length === 0 ? (
                  <div className="p-8 text-center text-gray-400">
                    <p className="text-sm">No data available</p>
                    <p className="text-xs mt-1">Connect your API to see data here</p>
                  </div>
                ) : (
                  <div className="divide-y divide-gray-100">
                    {{items.map((item) => (
                      <div
                        key={{item.id}}
                        className="px-4 py-3 flex items-center justify-between hover:bg-gray-50 transition-colors"
                      >
                        <div>
                          <p className="text-sm font-medium text-gray-900">{{item.name}}</p>
                          <p className="text-xs text-gray-400">{{item.id}}</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <span
                            className={{`text-xs px-2 py-1 rounded-full font-medium ${{
                              item.status === "active"
                                ? "bg-green-100 text-green-700"
                                : item.status === "error"
                                ? "bg-red-100 text-red-700"
                                : "bg-gray-100 text-gray-600"
                            }}`}}
                          >
                            {{item.status}}
                          </span>
                          <span className="text-xs text-gray-400">{{item.updatedAt}}</span>
                        </div>
                      </div>
                    ))}}
                  </div>
                )}}
              </div>
            </ErrorBoundary>
          );
        }}
    """)


def generate_loading_tsx(component_name: str) -> str:
    """Generate loading.tsx for Suspense fallback."""
    return dedent(f"""\
        import {{ LoadingSkeleton }} from "@/components/ui/LoadingSkeleton";

        export default function {component_name}Loading() {{
          return (
            <div className="max-w-7xl mx-auto p-4 md:p-6 lg:p-8 space-y-6">
              {{/* Header skeleton */}}
              <div className="space-y-2">
                <div className="skeleton h-8 w-48" />
                <div className="skeleton h-4 w-72" />
              </div>

              {{/* Cards skeleton */}}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <LoadingSkeleton variant="card" count={{3}} />
              </div>

              {{/* Content skeleton */}}
              <LoadingSkeleton variant="text" lines={{5}} />
            </div>
          );
        }}
    """)


def generate_error_tsx(component_name: str) -> str:
    """Generate error.tsx for route-level error handling."""
    return dedent(f"""\
        "use client";

        import {{ useEffect }} from "react";

        export default function {component_name}Error({{
          error,
          reset,
        }}: {{
          error: Error & {{ digest?: string }};
          reset: () => void;
        }}) {{
          useEffect(() => {{
            console.error("[{component_name}]", error);
          }}, [error]);

          return (
            <div className="max-w-lg mx-auto mt-16 p-8 text-center">
              <div className="bg-red-50 border border-red-200 rounded-lg p-8">
                <svg
                  className="w-12 h-12 text-red-400 mx-auto mb-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={{2}}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
                  />
                </svg>
                <h2 className="text-lg font-semibold text-red-800 mb-2">
                  Something went wrong
                </h2>
                <p className="text-sm text-red-600 mb-4">
                  {{error.message || "An unexpected error occurred on the {page_name} page."}}
                </p>
                <button
                  onClick={{reset}}
                  className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors text-sm font-medium"
                >
                  Try Again
                </button>
              </div>
            </div>
          );
        }}
    """.replace("{page_name}", component_name.lower()))


# ─── Page Generator ───────────────────────────────────────────────────────────

def generate_page(
    project_dir: str,
    page_name: str,
    with_monaco: bool,
    api_base_url: str,
    layout: str,
) -> tuple[bool, int]:
    """Generate all files for a single page. Returns (success, file_count)."""
    component_name = sanitize_page_name(page_name)
    page_dir = os.path.join(project_dir, "src", "app", "(routes)", page_name)

    # Idempotency: check if page already exists
    if os.path.isdir(page_dir) and os.path.isfile(os.path.join(page_dir, "page.tsx")):
        log("INFO", f"Page '{page_name}' already exists at {page_dir}, skipping")
        return True, 0

    os.makedirs(page_dir, exist_ok=True)
    file_count = 0

    try:
        # page.tsx
        page_content = generate_page_tsx(page_name, component_name, with_monaco, api_base_url, layout)
        write_file(os.path.join(page_dir, "page.tsx"), page_content)
        file_count += 1

        # Content component
        content = generate_content_component(component_name, page_name)
        write_file(os.path.join(page_dir, f"{component_name}Content.tsx"), content)
        file_count += 1

        # loading.tsx
        loading_content = generate_loading_tsx(component_name)
        write_file(os.path.join(page_dir, "loading.tsx"), loading_content)
        file_count += 1

        # error.tsx
        error_content = generate_error_tsx(component_name)
        write_file(os.path.join(page_dir, "error.tsx"), error_content)
        file_count += 1

        # Monaco editor component (optional)
        if with_monaco:
            editor_content = generate_editor_component(component_name)
            write_file(os.path.join(page_dir, f"{component_name}Editor.tsx"), editor_content)
            file_count += 1

        # API data component (optional, when api_base_url is set)
        if api_base_url:
            data_content = generate_data_component(component_name, api_base_url)
            write_file(os.path.join(page_dir, f"{component_name}Data.tsx"), data_content)
            file_count += 1

        log("INFO", f"Page '{page_name}' generated ({file_count} files)")
        return True, file_count

    except OSError as e:
        log("ERROR", f"Failed to generate page '{page_name}': {e}")
        return False, file_count


def write_file(filepath: str, content: str):
    """Write content to file, creating directories as needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    log("DEBUG", f"Wrote: {filepath}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate Next.js pages")
    parser.add_argument("--project-dir", default="./frontend-app", help="Project root directory")
    parser.add_argument("--pages", default="dashboard", help="Comma-separated page names")
    parser.add_argument("--with-monaco", action="store_true", help="Include Monaco editor")
    parser.add_argument("--api-base-url", default="/api", help="API base URL")
    parser.add_argument("--layout", default="sidebar", choices=["sidebar", "topnav", "minimal"], help="Layout type")
    args = parser.parse_args()

    pages = [p.strip().lower() for p in args.pages.split(",") if p.strip()]

    log("INFO", "=== Page Generation ===")
    log("INFO", f"Project: {args.project_dir} | Pages: {', '.join(pages)}")

    # Validate
    valid, error_msg = validate_inputs(args.project_dir, pages)
    if not valid:
        log("ERROR", error_msg)
        print(f"[ERROR] {error_msg}", file=sys.stderr)
        sys.exit(2)

    # Generate pages
    total_files = 0
    generated = []
    failed = []

    for page in pages:
        success, count = generate_page(
            project_dir=args.project_dir,
            page_name=page,
            with_monaco=args.with_monaco,
            api_base_url=args.api_base_url,
            layout=args.layout,
        )
        total_files += count
        if success:
            generated.append(page)
        else:
            failed.append(page)

    # Report
    if failed:
        print(f"[ERROR] Failed to generate: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)

    page_list = ", ".join(generated)
    print(f"[OK] Pages generated ({page_list})")
    sys.exit(0)


if __name__ == "__main__":
    main()
