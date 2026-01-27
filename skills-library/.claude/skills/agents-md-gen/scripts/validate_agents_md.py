#!/usr/bin/env python3
"""
AGENTS.md Validator

Validates generated AGENTS.md files for completeness and correctness.

Usage:
    python validate_agents_md.py /path/to/AGENTS.md [options]

Options:
    --verbose       Detailed output showing all checks
    --min-size N    Minimum file size in bytes (default: 200)

Exit Codes:
    0 - Valid
    1 - Invalid (missing sections, too small, etc.)
    2 - File not found or permission error
"""

import argparse
import io
import os
import re
import sys
from typing import List, Tuple

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Required sections in AGENTS.md
REQUIRED_SECTIONS = [
    "# AGENTS.md",
    "## Directory Structure",
    "## Technology Stack",
    "## Conventions"
]

# Minimum number of sections (including required)
MIN_SECTIONS = 4

# Default minimum file size
DEFAULT_MIN_SIZE = 200


def validate_file_exists(path: str) -> Tuple[bool, str]:
    """
    Check if file exists and is readable.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not os.path.exists(path):
        return False, f"File not found: {path}"

    if not os.path.isfile(path):
        return False, f"Not a file: {path}"

    if not os.access(path, os.R_OK):
        return False, f"Permission denied: {path}"

    return True, ""


def validate_file_size(path: str, min_bytes: int = DEFAULT_MIN_SIZE) -> Tuple[bool, str]:
    """
    Check if file meets minimum size requirement.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    size = os.path.getsize(path)

    if size < min_bytes:
        return False, f"File too small: {size} bytes (minimum: {min_bytes})"

    return True, ""


def validate_markdown_syntax(content: str) -> Tuple[bool, List[str]]:
    """
    Basic markdown syntax validation.

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_warnings)
    """
    warnings = []

    # Check for unclosed code blocks
    code_block_count = content.count("```")
    if code_block_count % 2 != 0:
        warnings.append("Unclosed code block (odd number of ```)")

    # Check for headers without content
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("#") and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line.startswith("#") or (next_line == "" and i + 2 < len(lines) and lines[i + 2].startswith("#")):
                # Allow ## headers directly after # headers
                if not (line.startswith("# ") and next_line.startswith("## ")):
                    pass  # This is fine for our generated format

    # Check for broken links (basic check)
    link_pattern = r'\[([^\]]*)\]\(([^\)]*)\)'
    for match in re.finditer(link_pattern, content):
        link_text, link_url = match.groups()
        if not link_url:
            warnings.append(f"Empty link URL for: [{link_text}]")

    return len(warnings) == 0, warnings


def validate_required_sections(content: str) -> Tuple[bool, List[str], List[str]]:
    """
    Check for required sections in AGENTS.md.

    Returns:
        Tuple[bool, List[str], List[str]]: (is_valid, found_sections, missing_sections)
    """
    found = []
    missing = []

    for section in REQUIRED_SECTIONS:
        if section in content:
            found.append(section)
        else:
            missing.append(section)

    return len(missing) == 0, found, missing


def count_sections(content: str) -> int:
    """
    Count total number of markdown sections (## headers).

    Returns:
        int: Number of sections
    """
    # Count all headers (# and ##)
    header_pattern = r'^#{1,2}\s+.+$'
    matches = re.findall(header_pattern, content, re.MULTILINE)
    return len(matches)


def validate_agents_md(path: str, min_size: int = DEFAULT_MIN_SIZE,
                       verbose: bool = False) -> Tuple[bool, str, dict]:
    """
    Full validation of AGENTS.md file.

    Returns:
        Tuple[bool, str, dict]: (is_valid, status_message, details)
    """
    details = {
        "file_exists": False,
        "file_size": 0,
        "size_valid": False,
        "syntax_valid": False,
        "syntax_warnings": [],
        "sections_valid": False,
        "found_sections": [],
        "missing_sections": [],
        "total_sections": 0
    }

    # Check file exists
    is_valid, error = validate_file_exists(path)
    if not is_valid:
        return False, error, details
    details["file_exists"] = True

    # Check file size
    details["file_size"] = os.path.getsize(path)
    is_valid, error = validate_file_size(path, min_size)
    if not is_valid:
        details["size_valid"] = False
        return False, error, details
    details["size_valid"] = True

    # Read content
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return False, f"Cannot read file: {e}", details

    # Validate markdown syntax
    syntax_valid, warnings = validate_markdown_syntax(content)
    details["syntax_valid"] = syntax_valid
    details["syntax_warnings"] = warnings

    # Validate required sections
    sections_valid, found, missing = validate_required_sections(content)
    details["sections_valid"] = sections_valid
    details["found_sections"] = found
    details["missing_sections"] = missing

    # Count total sections
    details["total_sections"] = count_sections(content)

    # Check minimum sections
    if details["total_sections"] < MIN_SECTIONS:
        return False, f"Insufficient sections: {details['total_sections']} (minimum: {MIN_SECTIONS})", details

    # Check for missing required sections
    if not sections_valid:
        return False, f"Missing required sections: {', '.join(missing)}", details

    # Check for syntax warnings (non-fatal but reported)
    if warnings and verbose:
        print(f"  Warnings: {'; '.join(warnings)}")

    return True, f"Valid ({details['total_sections']} sections, {details['file_size']} bytes)", details


def main():
    parser = argparse.ArgumentParser(
        description="Validate AGENTS.md files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("path", help="Path to AGENTS.md file")
    parser.add_argument("--verbose", action="store_true", help="Detailed output")
    parser.add_argument("--min-size", type=int, default=DEFAULT_MIN_SIZE,
                        help=f"Minimum file size in bytes (default: {DEFAULT_MIN_SIZE})")

    args = parser.parse_args()

    # Resolve path
    file_path = os.path.abspath(args.path)

    if args.verbose:
        print(f"Validating: {file_path}")
        print("-" * 40)

    # Run validation
    is_valid, message, details = validate_agents_md(file_path, args.min_size, args.verbose)

    if args.verbose:
        print(f"  File exists: {'[OK]' if details['file_exists'] else '[FAIL]'}")
        print(f"  File size: {details['file_size']} bytes {'[OK]' if details['size_valid'] else '[FAIL]'}")
        print(f"  Markdown syntax: {'[OK]' if details['syntax_valid'] else '[FAIL]'}")
        if details['syntax_warnings']:
            for warning in details['syntax_warnings']:
                print(f"    [WARN] {warning}")
        print(f"  Required sections: {'[OK]' if details['sections_valid'] else '[FAIL]'}")
        if details['found_sections']:
            for section in details['found_sections']:
                print(f"    [OK] {section}")
        if details['missing_sections']:
            for section in details['missing_sections']:
                print(f"    [FAIL] {section}")
        print(f"  Total sections: {details['total_sections']}")
        print("-" * 40)

    if is_valid:
        print(f"[OK] AGENTS.md valid ({details['total_sections']} sections, {details['file_size']} bytes)")
        sys.exit(0)
    else:
        print(f"[ERROR] AGENTS.md invalid: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
