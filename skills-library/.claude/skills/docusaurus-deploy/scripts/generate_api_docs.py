#!/usr/bin/env python3
"""generate_api_docs.py - Parse JSDoc/TSDoc/Python docstrings and generate Markdown API docs.

Scans source directories for TypeScript, JavaScript, and Python files. Extracts
documentation from JSDoc/TSDoc comment blocks (regex-based) and Python docstrings
(ast module, supporting Google/NumPy/Sphinx formats). Outputs Docusaurus-compatible
Markdown with front matter, parameter tables, return types, and code examples.

Exit codes:
    0 - Success
    1 - Fatal error
    2 - No source files found
    3 - Output directory not writable
"""

import argparse
import ast
import io
import json
import logging
import os
import re
import sys
import textwrap
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

LOG_FILE = os.environ.get("LOG_FILE", ".docusaurus-deploy.log")
logger = logging.getLogger("generate_api_docs")


def setup_logging(verbose: bool) -> None:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
    logger.addHandler(file_handler)

    if verbose:
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(stream_handler)

    logger.setLevel(logging.DEBUG)


# ---------------------------------------------------------------------------
# TypeScript / JavaScript JSDoc parsing
# ---------------------------------------------------------------------------

# Regex for /** ... */ blocks immediately followed by an export/function/class/const
JSDOC_BLOCK_RE = re.compile(
    r"/\*\*\s*\n([\s\S]*?)\*/\s*\n\s*"
    r"(?:export\s+)?(?:default\s+)?"
    r"(?:(?:async\s+)?function\s+(\w+)|class\s+(\w+)|(?:const|let|var)\s+(\w+))",
    re.MULTILINE,
)

TAG_RE = re.compile(r"@(\w+)\s*(.*)")


def _parse_jsdoc_block(raw: str) -> dict[str, Any]:
    """Parse the inside of a JSDoc comment block into structured data."""
    lines = [ln.strip().lstrip("* ").rstrip() for ln in raw.split("\n")]
    description_parts: list[str] = []
    params: list[dict[str, str]] = []
    returns = ""
    examples: list[str] = []
    tags: dict[str, str] = {}
    in_example = False
    example_buf: list[str] = []

    for line in lines:
        if in_example:
            if line.startswith("@") and not line.startswith("@example"):
                in_example = False
                examples.append("\n".join(example_buf))
                example_buf = []
            else:
                example_buf.append(line)
                continue

        m = TAG_RE.match(line)
        if m:
            tag_name, tag_val = m.group(1), m.group(2).strip()
            if tag_name == "param":
                pm = re.match(r"\{([^}]+)\}\s+(\w+)\s*[-–]?\s*(.*)", tag_val)
                if pm:
                    params.append({"type": pm.group(1), "name": pm.group(2), "desc": pm.group(3)})
                else:
                    pm2 = re.match(r"(\w+)\s*[-–]?\s*(.*)", tag_val)
                    if pm2:
                        params.append({"type": "any", "name": pm2.group(1), "desc": pm2.group(2)})
            elif tag_name == "returns" or tag_name == "return":
                rm = re.match(r"\{([^}]+)\}\s*(.*)", tag_val)
                returns = f"`{rm.group(1)}` {rm.group(2)}" if rm else tag_val
            elif tag_name == "example":
                in_example = True
                if tag_val:
                    example_buf.append(tag_val)
            else:
                tags[tag_name] = tag_val
        elif line:
            description_parts.append(line)

    if example_buf:
        examples.append("\n".join(example_buf))

    return {
        "description": " ".join(description_parts),
        "params": params,
        "returns": returns,
        "examples": examples,
        "tags": tags,
    }


def parse_ts_js_file(filepath: Path, include_private: bool) -> list[dict[str, Any]]:
    """Extract documented symbols from a TypeScript/JavaScript file."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        logger.warning("Cannot read %s: %s", filepath, exc)
        return []

    results: list[dict[str, Any]] = []
    for match in JSDOC_BLOCK_RE.finditer(content):
        raw_doc = match.group(1)
        name = match.group(2) or match.group(3) or match.group(4)
        if not name:
            continue
        if not include_private and name.startswith("_"):
            continue

        parsed = _parse_jsdoc_block(raw_doc)
        parsed["name"] = name
        parsed["file"] = str(filepath)
        parsed["language"] = "typescript" if filepath.suffix in (".ts", ".tsx") else "javascript"
        results.append(parsed)

    logger.debug("Parsed %d symbols from %s", len(results), filepath)
    return results


# ---------------------------------------------------------------------------
# Python docstring parsing
# ---------------------------------------------------------------------------

def _parse_python_docstring(raw: str) -> dict[str, Any]:
    """Parse a Python docstring (Google, NumPy, or Sphinx style)."""
    raw = textwrap.dedent(raw).strip()
    lines = raw.split("\n")

    description_parts: list[str] = []
    params: list[dict[str, str]] = []
    returns = ""
    examples: list[str] = []

    section = "desc"
    buf: list[str] = []

    for line in lines:
        stripped = line.strip()

        # Google style section headers
        if stripped in ("Args:", "Arguments:", "Parameters:", "Params:"):
            section = "params"
            continue
        if stripped in ("Returns:", "Return:"):
            section = "returns"
            continue
        if stripped in ("Examples:", "Example:"):
            section = "examples"
            continue
        if stripped in ("Raises:", "Yields:", "Attributes:", "Note:", "Notes:", "References:"):
            section = "skip"
            continue

        # NumPy style section headers (underlined with dashes)
        if stripped and set(stripped) == {"-"}:
            prev = buf[-1].strip() if buf else ""
            if prev.lower() in ("parameters", "args", "arguments"):
                section = "params"
                buf = []
                continue
            elif prev.lower() in ("returns", "return"):
                section = "returns"
                buf = []
                continue
            elif prev.lower() in ("examples", "example"):
                section = "examples"
                buf = []
                continue
            else:
                section = "skip"
                buf = []
                continue

        buf.append(line)

        if section == "desc":
            if stripped:
                description_parts.append(stripped)
        elif section == "params":
            # Google: name (type): description  OR  Sphinx: :param name: description
            gm = re.match(r"\s+(\w+)\s*\(([^)]+)\)\s*:\s*(.*)", line)
            sm = re.match(r"\s*:param\s+(\w+)\s*:\s*(.*)", line)
            nm = re.match(r"\s+(\w+)\s*:\s+(\w.*)", line)  # NumPy simple
            if gm:
                params.append({"name": gm.group(1), "type": gm.group(2), "desc": gm.group(3)})
            elif sm:
                params.append({"name": sm.group(1), "type": "Any", "desc": sm.group(2)})
            elif nm:
                params.append({"name": nm.group(1), "type": "Any", "desc": nm.group(2)})
        elif section == "returns":
            if stripped:
                returns += stripped + " "
        elif section == "examples":
            examples.append(line)

    return {
        "description": " ".join(description_parts),
        "params": params,
        "returns": returns.strip(),
        "examples": ["\n".join(examples)] if examples else [],
    }


def parse_python_file(filepath: Path, include_private: bool) -> list[dict[str, Any]]:
    """Extract documented symbols from a Python file using ast."""
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        logger.warning("Cannot read %s: %s", filepath, exc)
        return []

    try:
        tree = ast.parse(source, filename=str(filepath))
    except SyntaxError as exc:
        logger.warning("Syntax error in %s: %s", filepath, exc)
        return []

    results: list[dict[str, Any]] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
            if not include_private and name.startswith("_") and not name.startswith("__"):
                continue

            docstring = ast.get_docstring(node)
            if not docstring:
                continue

            parsed = _parse_python_docstring(docstring)
            parsed["name"] = name
            parsed["file"] = str(filepath)
            parsed["language"] = "python"
            parsed["kind"] = "class" if isinstance(node, ast.ClassDef) else "function"
            results.append(parsed)

    logger.debug("Parsed %d symbols from %s", len(results), filepath)
    return results


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def _generate_markdown(symbol: dict[str, Any], position: int) -> str:
    """Generate Docusaurus-compatible Markdown for a single symbol."""
    slug = symbol["name"].lower().replace("_", "-")
    kind = symbol.get("kind", "function")
    lang = symbol["language"]

    lines = [
        "---",
        f"title: {symbol['name']}",
        f"sidebar_label: {symbol['name']}",
        f"sidebar_position: {position}",
        f"description: \"{symbol['description'][:160]}\"" if symbol["description"] else "",
        "---",
        "",
        f"# `{symbol['name']}`",
        "",
        f"**Kind:** {kind} &middot; **Language:** {lang} &middot; **Source:** `{symbol['file']}`",
        "",
    ]

    if symbol["description"]:
        lines.append(symbol["description"])
        lines.append("")

    if symbol.get("params"):
        lines.append("## Parameters")
        lines.append("")
        lines.append("| Name | Type | Description |")
        lines.append("|------|------|-------------|")
        for p in symbol["params"]:
            lines.append(f"| `{p['name']}` | `{p['type']}` | {p['desc']} |")
        lines.append("")

    if symbol.get("returns"):
        lines.append("## Returns")
        lines.append("")
        lines.append(symbol["returns"])
        lines.append("")

    if symbol.get("examples"):
        lines.append("## Examples")
        lines.append("")
        for ex in symbol["examples"]:
            lines.append(f"```{lang}")
            lines.append(ex.strip())
            lines.append("```")
            lines.append("")

    # Filter out empty description line in frontmatter
    return "\n".join(ln for ln in lines if ln is not None and ln != 'description: ""')


def _generate_category_json(label: str, position: int) -> str:
    return json.dumps(
        {
            "label": label,
            "position": position,
            "link": {"type": "generated-index", "description": f"Auto-generated {label} documentation."},
        },
        indent=2,
    )


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def collect_files(source_dirs: list[str], languages: list[str]) -> list[Path]:
    exts: set[str] = set()
    if "typescript" in languages or "ts" in languages:
        exts.update({".ts", ".tsx"})
    if "javascript" in languages or "js" in languages:
        exts.update({".js", ".jsx"})
    if "python" in languages or "py" in languages:
        exts.add(".py")

    files: list[Path] = []
    for sd in source_dirs:
        sd_path = Path(sd)
        if not sd_path.is_dir():
            logger.warning("Source directory does not exist: %s", sd)
            continue
        for f in sd_path.rglob("*"):
            if f.suffix in exts and f.is_file():
                # Skip node_modules, __pycache__, dist, build
                parts = f.parts
                if any(p in ("node_modules", "__pycache__", "dist", "build", ".git") for p in parts):
                    continue
                files.append(f)

    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate API docs from source code.")
    parser.add_argument("--source-dirs", nargs="+", required=True, help="Directories to scan")
    parser.add_argument("--output-dir", required=True, help="Output directory for Markdown files")
    parser.add_argument("--languages", nargs="+", default=["typescript", "javascript", "python"],
                        help="Languages to parse")
    parser.add_argument("--include-private", action="store_true", help="Include private symbols")
    parser.add_argument("--group-by", choices=["file", "module", "flat"], default="module",
                        help="Grouping strategy")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be generated")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger.info("=== API docs generation started ===")

    output_path = Path(args.output_dir)
    if not args.dry_run:
        try:
            output_path.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            logger.error("Cannot create output directory: %s", exc)
            sys.exit(3)

    files = collect_files(args.source_dirs, args.languages)
    if not files:
        logger.error("No source files found in %s for languages %s", args.source_dirs, args.languages)
        sys.exit(2)

    logger.info("Found %d source files to scan", len(files))

    all_symbols: list[dict[str, Any]] = []
    for f in files:
        if f.suffix in (".ts", ".tsx", ".js", ".jsx"):
            all_symbols.extend(parse_ts_js_file(f, args.include_private))
        elif f.suffix == ".py":
            all_symbols.extend(parse_python_file(f, args.include_private))

    if not all_symbols:
        logger.warning("No documented symbols found")
        print("[OK] API docs generated (files: 0, symbols: 0)")
        sys.exit(0)

    logger.info("Found %d documented symbols", len(all_symbols))

    if args.dry_run:
        for s in all_symbols:
            print(f"  {s['language']}:{s['name']} ({s['file']})")
        print(f"[DRY-RUN] Would generate {len(all_symbols)} doc files")
        sys.exit(0)

    # Group by module (parent directory relative to source root)
    groups: dict[str, list[dict[str, Any]]] = {}
    if args.group_by == "flat":
        groups["api"] = all_symbols
    else:
        for sym in all_symbols:
            fp = Path(sym["file"])
            group_key = fp.parent.name if args.group_by == "module" else fp.stem
            groups.setdefault(group_key, []).append(sym)

    files_written = 0
    for group_name, symbols in sorted(groups.items()):
        group_dir = output_path / group_name if args.group_by != "flat" else output_path
        group_dir.mkdir(parents=True, exist_ok=True)

        # Write category JSON
        if args.group_by != "flat":
            cat_file = group_dir / "_category_.json"
            cat_file.write_text(
                _generate_category_json(group_name.replace("_", " ").title(), files_written + 1),
                encoding="utf-8",
            )

        for idx, sym in enumerate(symbols, start=1):
            md_content = _generate_markdown(sym, idx)
            md_file = group_dir / f"{sym['name'].lower().replace('_', '-')}.md"
            md_file.write_text(md_content, encoding="utf-8")
            files_written += 1

    logger.info("=== API docs generation complete ===")
    print(f"[OK] API docs generated (files: {files_written}, symbols: {len(all_symbols)})")


if __name__ == "__main__":
    main()
