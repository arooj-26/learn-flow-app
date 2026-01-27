#!/usr/bin/env python3
"""generate_skill_docs.py - Auto-document the skills library for Docusaurus.

Scans a skills directory for SKILL.md files, parses YAML frontmatter (name,
description, version), extracts instruction sections, and optionally embeds
REFERENCE.md content. Generates a browsable Docusaurus docs section with a
skills index page containing a summary table.

Exit codes:
    0 - Success
    1 - Fatal error
    2 - No skills found
    3 - Output directory not writable
"""

import argparse
import io
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

LOG_FILE = os.environ.get("LOG_FILE", ".docusaurus-deploy.log")
logger = logging.getLogger("generate_skill_docs")


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
# YAML frontmatter parsing (with or without PyYAML)
# ---------------------------------------------------------------------------

def _parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Return (frontmatter_dict, body) from a Markdown file with YAML frontmatter."""
    if not content.startswith("---"):
        return {}, content

    end = content.find("---", 3)
    if end == -1:
        return {}, content

    raw_yaml = content[3:end].strip()
    body = content[end + 3:].strip()

    if yaml is not None:
        try:
            fm = yaml.safe_load(raw_yaml) or {}
        except yaml.YAMLError as exc:
            logger.warning("YAML parse error: %s", exc)
            fm = {}
    else:
        # Fallback: naive key: value parsing
        fm = {}
        for line in raw_yaml.split("\n"):
            m = re.match(r"^(\w[\w-]*):\s*(.+)", line)
            if m:
                key = m.group(1)
                val = m.group(2).strip().strip('"').strip("'")
                fm[key] = val

    return fm, body


# ---------------------------------------------------------------------------
# Skill discovery
# ---------------------------------------------------------------------------

def discover_skills(skills_dir: Path) -> list[dict[str, Any]]:
    """Find all SKILL.md files and parse them."""
    skills: list[dict[str, Any]] = []

    for skill_md in sorted(skills_dir.rglob("SKILL.md")):
        skill_dir = skill_md.parent
        name = skill_dir.name

        try:
            content = skill_md.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            logger.warning("Cannot read %s: %s", skill_md, exc)
            continue

        fm, body = _parse_frontmatter(content)

        # Check for REFERENCE.md
        ref_path = skill_dir / "REFERENCE.md"
        reference = ""
        if ref_path.is_file():
            try:
                reference = ref_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass

        # Check for scripts
        scripts_dir = skill_dir / "scripts"
        scripts: list[str] = []
        if scripts_dir.is_dir():
            scripts = sorted(
                f.name for f in scripts_dir.iterdir()
                if f.is_file() and f.name != "requirements.txt" and f.name != "__pycache__"
            )

        skills.append({
            "name": fm.get("name", name),
            "dir_name": name,
            "description": fm.get("description", ""),
            "version": fm.get("version", ""),
            "body": body,
            "reference": reference,
            "scripts": scripts,
            "path": str(skill_md),
        })

    return skills


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def _generate_index_page(skills: list[dict[str, Any]]) -> str:
    """Generate an index page with a skills summary table."""
    lines = [
        "---",
        "title: Skills Library",
        "sidebar_label: Overview",
        "sidebar_position: 1",
        "description: Index of all available skills in the library.",
        "---",
        "",
        "# Skills Library",
        "",
        "This section contains auto-generated documentation for all skills in the library.",
        "",
        "## Available Skills",
        "",
        "| Skill | Version | Description |",
        "|-------|---------|-------------|",
    ]

    for s in skills:
        link = f"[{s['name']}](./{s['dir_name']})"
        lines.append(f"| {link} | {s.get('version', '-')} | {s.get('description', '-')} |")

    lines.append("")
    lines.append(f"**Total skills:** {len(skills)}")
    lines.append("")
    return "\n".join(lines)


def _generate_skill_page(skill: dict[str, Any], position: int,
                         include_scripts: bool, include_reference: bool) -> str:
    """Generate a Docusaurus doc page for a single skill."""
    lines = [
        "---",
        f"title: {skill['name']}",
        f"sidebar_label: {skill['name']}",
        f"sidebar_position: {position}",
    ]
    if skill["description"]:
        desc = skill["description"].replace('"', '\\"')[:160]
        lines.append(f'description: "{desc}"')
    lines.extend(["---", ""])

    # Skill body (original SKILL.md content minus frontmatter)
    if skill["body"]:
        lines.append(skill["body"])
        lines.append("")

    # Scripts listing
    if include_scripts and skill["scripts"]:
        lines.append("## Scripts")
        lines.append("")
        lines.append("| Script | Description |")
        lines.append("|--------|-------------|")
        for s in skill["scripts"]:
            lines.append(f"| `{s}` | Part of the {skill['name']} skill |")
        lines.append("")

    # Reference content
    if include_reference and skill["reference"]:
        lines.append("---")
        lines.append("")
        lines.append("## Reference")
        lines.append("")
        # Strip any frontmatter from reference
        _, ref_body = _parse_frontmatter(skill["reference"])
        lines.append(ref_body)
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate skill library documentation.")
    parser.add_argument("--skills-dir", required=True, help="Root skills directory to scan")
    parser.add_argument("--output-dir", required=True, help="Output directory for Markdown files")
    parser.add_argument("--include-scripts", action="store_true", help="Include script listings")
    parser.add_argument("--include-reference", action="store_true", help="Embed REFERENCE.md content")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger.info("=== Skill docs generation started ===")

    skills_path = Path(args.skills_dir)
    if not skills_path.is_dir():
        logger.error("Skills directory does not exist: %s", args.skills_dir)
        sys.exit(2)

    output_path = Path(args.output_dir)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        logger.error("Cannot create output directory: %s", exc)
        sys.exit(3)

    skills = discover_skills(skills_path)
    if not skills:
        logger.error("No skills found in %s", args.skills_dir)
        sys.exit(2)

    logger.info("Found %d skills", len(skills))

    # Write category JSON
    cat_file = output_path / "_category_.json"
    cat_file.write_text(
        json.dumps(
            {
                "label": "Skills Library",
                "position": 3,
                "link": {"type": "generated-index", "description": "Auto-generated skill documentation."},
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Write index page
    index_content = _generate_index_page(skills)
    (output_path / "index.md").write_text(index_content, encoding="utf-8")

    # Write individual skill pages
    for idx, skill in enumerate(skills, start=2):
        page = _generate_skill_page(
            skill, idx,
            include_scripts=args.include_scripts,
            include_reference=args.include_reference,
        )
        filename = f"{skill['dir_name']}.md"
        (output_path / filename).write_text(page, encoding="utf-8")
        logger.debug("Wrote %s", filename)

    logger.info("=== Skill docs generation complete ===")
    print(f"[OK] Skill docs generated (skills: {len(skills)}, files: {len(skills) + 1})")


if __name__ == "__main__":
    main()
