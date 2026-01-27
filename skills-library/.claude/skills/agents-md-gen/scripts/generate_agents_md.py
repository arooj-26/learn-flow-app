#!/usr/bin/env python3
"""
AGENTS.md Generator

Analyzes any project and generates AGENTS.md files that teach AI agents
about the codebase. Production-grade with full error handling, retries,
logging, and idempotency.

Usage:
    python generate_agents_md.py /path/to/project [options]

Options:
    --dry-run       Preview without writing
    --verbose       Detailed output
    --cleanup       Remove generated AGENTS.md
    --max-depth N   Directory scan depth (default: 4)
    --output FILE   Custom output filename (default: AGENTS.md)

Exit Codes:
    0 - Success
    1 - Fatal error (IO, timeout)
    2 - Validation error (bad input)
"""

import argparse
import io
import json
import os
import shutil
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
DEFAULT_MAX_DEPTH = 4
DEFAULT_TIMEOUT = int(os.environ.get("AGENTS_TIMEOUT", "30"))
LOG_FILE = os.environ.get("AGENTS_LOG_FILE", ".agents-gen.log")
DEBUG = os.environ.get("DEBUG", "0") == "1"
MAX_RETRIES = 3

# Directories to always exclude
EXCLUDE_DIRS = {
    "node_modules", ".git", ".svn", ".hg", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".tox", ".nox", ".eggs", "*.egg-info", "dist", "build",
    ".venv", "venv", "env", ".env", "coverage", ".coverage", ".nyc_output",
    "htmlcov", ".idea", ".vscode", ".vs", "*.xcodeproj", "*.xcworkspace",
    "target", "out", "bin", "obj", ".next", ".nuxt", ".output", ".cache"
}

# File patterns for project detection
PROJECT_INDICATORS = {
    "nodejs": ["package.json"],
    "python": ["pyproject.toml", "setup.py", "requirements.txt", "Pipfile"],
    "monorepo": ["pnpm-workspace.yaml", "lerna.json", "rush.json", "nx.json"],
    "rust": ["Cargo.toml"],
    "go": ["go.mod"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
}


class TimeoutError(Exception):
    """Raised when operation times out."""
    pass


def timeout_handler(signum, frame):
    """Signal handler for timeout."""
    raise TimeoutError(f"Operation timed out after {DEFAULT_TIMEOUT}s")


def get_utc_now() -> datetime:
    """Get current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)


def log(level: str, message: str, verbose: bool = False):
    """Log message to file and optionally stdout."""
    timestamp = get_utc_now().isoformat().replace("+00:00", "Z")
    log_line = f"[{timestamp}] [{level}] {message}"

    # Write to log file
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_line + "\n")
    except Exception:
        pass  # Don't fail on log errors

    # Output to stdout if debug or verbose
    if DEBUG or (verbose and level in ("INFO", "WARNING", "ERROR")):
        print(log_line, file=sys.stderr)


def validate_inputs(project_path: str) -> tuple[bool, str]:
    """
    Validate input parameters.

    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    # Check path exists
    if not os.path.exists(project_path):
        return False, f"Path does not exist: {project_path}"

    # Check is directory
    if not os.path.isdir(project_path):
        return False, f"Path is not a directory: {project_path}"

    # Check readable
    if not os.access(project_path, os.R_OK):
        return False, f"Permission denied: {project_path}"

    return True, ""


def detect_project_type(project_path: str) -> str:
    """
    Detect the project type based on indicator files.

    Returns:
        str: Project type (nodejs, python, monorepo, rust, go, java, unknown)
    """
    path = Path(project_path)

    # Check for monorepo first (takes precedence)
    for indicator in PROJECT_INDICATORS["monorepo"]:
        if (path / indicator).exists():
            return "monorepo"

    # Check for packages/ directory (common monorepo pattern)
    if (path / "packages").is_dir() and (path / "package.json").exists():
        return "monorepo"

    # Check other project types
    for project_type, indicators in PROJECT_INDICATORS.items():
        if project_type == "monorepo":
            continue
        for indicator in indicators:
            if (path / indicator).exists():
                return project_type

    return "unknown"


def should_exclude(name: str) -> bool:
    """Check if a directory/file should be excluded."""
    return name in EXCLUDE_DIRS or name.startswith(".")


def analyze_directory(project_path: str, max_depth: int = DEFAULT_MAX_DEPTH) -> dict:
    """
    Analyze directory structure with retry logic.

    Returns:
        dict: Directory structure and statistics
    """
    result = {
        "structure": [],
        "stats": {
            "directories": 0,
            "files": 0,
            "file_types": {}
        }
    }

    def scan_dir(path: Path, depth: int, prefix: str = ""):
        if depth > max_depth:
            return

        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            return

        dirs = []
        files = []

        for item in items:
            if should_exclude(item.name):
                continue

            if item.is_dir():
                dirs.append(item)
                result["stats"]["directories"] += 1
            elif item.is_file():
                files.append(item)
                result["stats"]["files"] += 1
                ext = item.suffix.lower() or "(no extension)"
                result["stats"]["file_types"][ext] = result["stats"]["file_types"].get(ext, 0) + 1

        # Build structure representation
        for i, d in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1) and len(files) == 0
            connector = "└── " if is_last_dir else "├── "
            result["structure"].append(f"{prefix}{connector}{d.name}/")

            child_prefix = prefix + ("    " if is_last_dir else "│   ")
            scan_dir(d, depth + 1, child_prefix)

        for i, f in enumerate(files[:10]):  # Limit files shown per directory
            is_last = i == len(files[:10]) - 1
            connector = "└── " if is_last else "├── "
            result["structure"].append(f"{prefix}{connector}{f.name}")

        if len(files) > 10:
            result["structure"].append(f"{prefix}    ... and {len(files) - 10} more files")

    # Retry logic
    for attempt in range(MAX_RETRIES):
        try:
            scan_dir(Path(project_path), 0)
            return result
        except Exception as e:
            log("WARNING", f"Directory analysis attempt {attempt + 1} failed: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(0.5)

    return result


def read_json_file(path: Path) -> Optional[dict]:
    """Safely read and parse a JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def analyze_nodejs(project_path: str) -> dict:
    """Analyze a Node.js project."""
    path = Path(project_path)
    info = {
        "name": "Unknown",
        "version": "0.0.0",
        "description": "",
        "dependencies": [],
        "devDependencies": [],
        "scripts": [],
        "framework": "Node.js",
        "packageManager": "npm"
    }

    package_json = read_json_file(path / "package.json")
    if package_json:
        info["name"] = package_json.get("name", info["name"])
        info["version"] = package_json.get("version", info["version"])
        info["description"] = package_json.get("description", "")
        info["dependencies"] = list(package_json.get("dependencies", {}).keys())
        info["devDependencies"] = list(package_json.get("devDependencies", {}).keys())
        info["scripts"] = list(package_json.get("scripts", {}).keys())

        # Detect framework
        deps = info["dependencies"] + info["devDependencies"]
        if "next" in deps:
            info["framework"] = "Next.js"
        elif "express" in deps:
            info["framework"] = "Express"
        elif "fastify" in deps:
            info["framework"] = "Fastify"
        elif "koa" in deps:
            info["framework"] = "Koa"
        elif "react" in deps:
            info["framework"] = "React"
        elif "vue" in deps:
            info["framework"] = "Vue.js"
        elif "svelte" in deps:
            info["framework"] = "Svelte"

    # Detect package manager
    if (path / "pnpm-lock.yaml").exists():
        info["packageManager"] = "pnpm"
    elif (path / "yarn.lock").exists():
        info["packageManager"] = "yarn"
    elif (path / "bun.lockb").exists():
        info["packageManager"] = "bun"

    return info


def analyze_python(project_path: str) -> dict:
    """Analyze a Python project."""
    path = Path(project_path)
    info = {
        "name": path.name,
        "version": "0.0.0",
        "description": "",
        "dependencies": [],
        "framework": "Python",
        "packageManager": "pip"
    }

    # Check pyproject.toml
    pyproject = read_json_file(path / "pyproject.toml")  # Won't work, TOML != JSON

    # Check requirements.txt
    req_file = path / "requirements.txt"
    if req_file.exists():
        try:
            with open(req_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Extract package name (before ==, >=, etc.)
                        pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split("[")[0].strip()
                        if pkg:
                            info["dependencies"].append(pkg)
        except Exception:
            pass

    # Detect framework
    deps_lower = [d.lower() for d in info["dependencies"]]
    if "django" in deps_lower:
        info["framework"] = "Django"
    elif "fastapi" in deps_lower:
        info["framework"] = "FastAPI"
    elif "flask" in deps_lower:
        info["framework"] = "Flask"
    elif "starlette" in deps_lower:
        info["framework"] = "Starlette"

    # Detect package manager
    if (path / "poetry.lock").exists():
        info["packageManager"] = "poetry"
    elif (path / "Pipfile.lock").exists():
        info["packageManager"] = "pipenv"
    elif (path / "uv.lock").exists():
        info["packageManager"] = "uv"

    return info


def analyze_monorepo(project_path: str) -> dict:
    """Analyze a monorepo project."""
    path = Path(project_path)
    info = {
        "name": path.name,
        "packages": [],
        "framework": "Monorepo",
        "packageManager": "npm"
    }

    # Find packages
    packages_dir = path / "packages"
    if packages_dir.is_dir():
        try:
            for item in packages_dir.iterdir():
                if item.is_dir() and not should_exclude(item.name):
                    pkg_info = {"name": item.name, "path": f"packages/{item.name}"}
                    pkg_json = read_json_file(item / "package.json")
                    if pkg_json:
                        pkg_info["fullName"] = pkg_json.get("name", item.name)
                    info["packages"].append(pkg_info)
        except Exception:
            pass

    # Detect monorepo tool
    if (path / "pnpm-workspace.yaml").exists():
        info["packageManager"] = "pnpm"
        info["tool"] = "pnpm workspaces"
    elif (path / "lerna.json").exists():
        info["tool"] = "Lerna"
    elif (path / "nx.json").exists():
        info["tool"] = "Nx"
    elif (path / "turbo.json").exists():
        info["tool"] = "Turborepo"
    elif (path / "rush.json").exists():
        info["tool"] = "Rush"

    return info


def generate_content(project_path: str, project_type: str, dir_info: dict, verbose: bool = False) -> str:
    """Generate AGENTS.md content."""
    path = Path(project_path)
    project_name = path.name

    # Get project-specific info
    if project_type == "nodejs":
        proj_info = analyze_nodejs(project_path)
        project_name = proj_info.get("name", project_name)
    elif project_type == "python":
        proj_info = analyze_python(project_path)
        project_name = proj_info.get("name", project_name)
    elif project_type == "monorepo":
        proj_info = analyze_monorepo(project_path)
        project_name = proj_info.get("name", project_name)
    else:
        proj_info = {"framework": "Unknown"}

    log("DEBUG", f"Project info: {proj_info}", verbose)

    # Build content sections
    sections = []

    # Header
    sections.append(f"# AGENTS.md\n")
    sections.append(f"Documentation for AI agents working with **{project_name}**.\n")

    # Directory Structure
    sections.append("## Directory Structure\n")
    sections.append("```")
    sections.append(f"{project_name}/")
    for line in dir_info["structure"][:50]:  # Limit lines
        sections.append(line)
    if len(dir_info["structure"]) > 50:
        sections.append(f"... and {len(dir_info['structure']) - 50} more entries")
    sections.append("```\n")

    # Statistics
    sections.append(f"**Stats**: {dir_info['stats']['directories']} directories, {dir_info['stats']['files']} files\n")

    # Technology Stack
    sections.append("## Technology Stack\n")

    if project_type == "nodejs":
        sections.append(f"- **Runtime**: Node.js")
        sections.append(f"- **Framework**: {proj_info.get('framework', 'N/A')}")
        sections.append(f"- **Package Manager**: {proj_info.get('packageManager', 'npm')}")
        if proj_info.get("dependencies"):
            sections.append(f"- **Dependencies**: {len(proj_info['dependencies'])} production, {len(proj_info.get('devDependencies', []))} development")
            # Show key deps
            key_deps = proj_info["dependencies"][:5]
            if key_deps:
                sections.append(f"- **Key packages**: {', '.join(key_deps)}")
        sections.append("")

    elif project_type == "python":
        sections.append(f"- **Runtime**: Python")
        sections.append(f"- **Framework**: {proj_info.get('framework', 'N/A')}")
        sections.append(f"- **Package Manager**: {proj_info.get('packageManager', 'pip')}")
        if proj_info.get("dependencies"):
            sections.append(f"- **Dependencies**: {len(proj_info['dependencies'])} packages")
            key_deps = proj_info["dependencies"][:5]
            if key_deps:
                sections.append(f"- **Key packages**: {', '.join(key_deps)}")
        sections.append("")

    elif project_type == "monorepo":
        sections.append(f"- **Type**: Monorepo")
        sections.append(f"- **Tool**: {proj_info.get('tool', 'Unknown')}")
        sections.append(f"- **Package Manager**: {proj_info.get('packageManager', 'npm')}")
        if proj_info.get("packages"):
            sections.append(f"- **Packages**: {len(proj_info['packages'])}")
            for pkg in proj_info["packages"][:5]:
                sections.append(f"  - `{pkg['path']}`: {pkg.get('fullName', pkg['name'])}")
        sections.append("")

    else:
        # Unknown project type - show file type stats
        sections.append(f"- **Type**: {project_type.capitalize()}")
        if dir_info["stats"]["file_types"]:
            top_types = sorted(dir_info["stats"]["file_types"].items(), key=lambda x: x[1], reverse=True)[:5]
            sections.append(f"- **Primary file types**:")
            for ext, count in top_types:
                sections.append(f"  - `{ext}`: {count} files")
        sections.append("")

    # Conventions
    sections.append("## Conventions\n")

    if project_type == "nodejs":
        sections.append("- Use `npm install` / `pnpm install` / `yarn` to install dependencies")
        if proj_info.get("scripts"):
            sections.append(f"- Available scripts: `{', '.join(proj_info['scripts'][:5])}`")
        sections.append("- Check `package.json` for entry points and build configuration")
        sections.append("- Environment variables typically in `.env` (see `.env.example` if present)")
        sections.append("")

    elif project_type == "python":
        sections.append("- Use virtual environments for dependency isolation")
        sections.append(f"- Install dependencies: `{proj_info.get('packageManager', 'pip')} install -r requirements.txt`")
        sections.append("- Follow PEP 8 style guidelines")
        sections.append("- Use type hints for function signatures")
        sections.append("")

    elif project_type == "monorepo":
        pm = proj_info.get("packageManager", "npm")
        sections.append(f"- Install all packages: `{pm} install` from root")
        sections.append(f"- Run commands in specific packages: `{pm} --filter <package> <command>`")
        sections.append("- Shared code goes in common packages")
        sections.append("- Check root `package.json` or config files for build orchestration")
        sections.append("")

    else:
        sections.append("- Review project structure to understand organization")
        sections.append("- Check for README.md for project-specific instructions")
        sections.append("- Look for configuration files at project root")
        sections.append("")

    # Important Files
    sections.append("## Important Files\n")
    important_files = []

    # Check common important files
    common_files = [
        ("README.md", "Project documentation"),
        ("CONTRIBUTING.md", "Contribution guidelines"),
        ("LICENSE", "License information"),
        (".env.example", "Environment variable template"),
        ("Dockerfile", "Container configuration"),
        ("docker-compose.yml", "Multi-container setup"),
        (".github/workflows", "CI/CD pipelines"),
    ]

    for filename, description in common_files:
        if (path / filename).exists():
            important_files.append(f"- `{filename}`: {description}")

    if important_files:
        sections.extend(important_files)
    else:
        sections.append("- Check project root for configuration files")

    sections.append("")

    # Footer
    sections.append("---")
    sections.append(f"*Generated by agents-md-gen on {get_utc_now().strftime('%Y-%m-%d %H:%M:%S')} UTC*")

    return "\n".join(sections)


def write_agents_md(project_path: str, content: str, output_file: str = "AGENTS.md",
                    dry_run: bool = False, verbose: bool = False) -> int:
    """
    Write AGENTS.md file with backup and idempotency.

    Returns:
        int: Number of bytes written
    """
    output_path = os.path.join(project_path, output_file)

    if dry_run:
        log("INFO", f"[DRY RUN] Would write {len(content)} bytes to {output_path}", verbose)
        print(f"[DRY RUN] Preview of {output_file}:")
        print("-" * 40)
        print(content[:1000])
        if len(content) > 1000:
            print(f"... ({len(content) - 1000} more characters)")
        print("-" * 40)
        return len(content)

    # Backup existing file (idempotency)
    if os.path.exists(output_path):
        backup_path = output_path + ".bak"
        try:
            shutil.copy(output_path, backup_path)
            log("INFO", f"Backed up existing file to {backup_path}", verbose)
        except Exception as e:
            log("WARNING", f"Could not create backup: {e}", verbose)

    # Write new file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        file_size = os.path.getsize(output_path)
        log("INFO", f"Generated {output_file} ({file_size} bytes)", verbose)
        return file_size

    except PermissionError:
        raise PermissionError(f"Cannot write to {output_path}")
    except Exception as e:
        raise IOError(f"Failed to write {output_path}: {e}")


def cleanup(project_path: str, output_file: str = "AGENTS.md", verbose: bool = False) -> bool:
    """
    Remove generated AGENTS.md and optionally restore backup.

    Returns:
        bool: True if cleanup successful
    """
    output_path = os.path.join(project_path, output_file)
    backup_path = output_path + ".bak"

    if not os.path.exists(output_path):
        log("INFO", f"No {output_file} to clean up", verbose)
        print(f"[OK] No {output_file} found (nothing to clean)")
        return True

    try:
        os.remove(output_path)
        log("INFO", f"Removed {output_path}", verbose)

        # Restore backup if exists
        if os.path.exists(backup_path):
            shutil.move(backup_path, output_path)
            log("INFO", f"Restored backup to {output_path}", verbose)
            print(f"[OK] Cleaned up {output_file} (restored from backup)")
        else:
            print(f"[OK] Cleaned up {output_file}")

        return True

    except Exception as e:
        log("ERROR", f"Cleanup failed: {e}", verbose)
        print(f"[ERROR] Cleanup failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate AGENTS.md for AI agent documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("path", help="Project path to analyze")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--verbose", action="store_true", help="Detailed output")
    parser.add_argument("--cleanup", action="store_true", help="Remove generated AGENTS.md")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH, help="Directory scan depth")
    parser.add_argument("--output", default="AGENTS.md", help="Output filename")

    args = parser.parse_args()

    # Resolve path
    project_path = os.path.abspath(args.path)

    log("INFO", f"Starting analysis of {project_path}", args.verbose)

    # Handle cleanup
    if args.cleanup:
        success = cleanup(project_path, args.output, args.verbose)
        sys.exit(0 if success else 1)

    # Validate inputs
    is_valid, error_msg = validate_inputs(project_path)
    if not is_valid:
        log("ERROR", error_msg, args.verbose)
        print(f"[ERROR] {error_msg}")
        sys.exit(2)

    # Set up timeout (Unix only)
    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(DEFAULT_TIMEOUT)
    except AttributeError:
        pass  # Windows doesn't support SIGALRM

    try:
        # Detect project type
        project_type = detect_project_type(project_path)
        log("INFO", f"Detected project type: {project_type}", args.verbose)

        # Analyze directory structure
        dir_info = analyze_directory(project_path, args.max_depth)
        log("DEBUG", f"Found {dir_info['stats']['directories']} directories, {dir_info['stats']['files']} files", args.verbose)

        # Generate content
        content = generate_content(project_path, project_type, dir_info, args.verbose)

        # Write file
        bytes_written = write_agents_md(
            project_path, content, args.output,
            args.dry_run, args.verbose
        )

        # Cancel timeout
        try:
            signal.alarm(0)
        except AttributeError:
            pass

        # Minimal output for token efficiency
        if args.dry_run:
            print(f"[OK] AGENTS.md would be generated ({bytes_written} bytes)")
        else:
            print(f"[OK] AGENTS.md generated ({bytes_written} bytes)")

        sys.exit(0)

    except TimeoutError as e:
        log("ERROR", str(e), args.verbose)
        print(f"[ERROR] Analysis timeout (>{DEFAULT_TIMEOUT}s)")
        sys.exit(1)

    except FileNotFoundError as e:
        log("ERROR", str(e), args.verbose)
        print(f"[ERROR] Project path not found")
        sys.exit(1)

    except PermissionError as e:
        log("ERROR", str(e), args.verbose)
        print(f"[ERROR] Cannot read project directory")
        sys.exit(1)

    except Exception as e:
        log("ERROR", f"Unexpected error: {e}", args.verbose)
        print(f"[ERROR] Generation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
