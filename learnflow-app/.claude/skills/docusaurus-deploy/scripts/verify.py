#!/usr/bin/env python3
"""verify.py - Verify a Docusaurus documentation deployment.

Runs 7 verification tests:
    1. Build output exists (index.html, sitemap.xml)
    2. Search index generated (local file or Algolia API)
    3. API docs present (docs/api/ has .md files)
    4. Skill docs present (docs/skills/ has .md files)
    5. Site accessible (HTTP 200 at deployed URL)
    6. Internal links valid (no broken hrefs)
    7. Performance metrics (build size < 20MB, largest asset < 5MB)

Exit codes:
    0 - All tests passed
    1 - One or more tests failed
    2 - Configuration error
"""

import argparse
import io
import logging
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

LOG_FILE = os.environ.get("LOG_FILE", ".docusaurus-deploy.log")
logger = logging.getLogger("verify")

# Thresholds
MAX_BUILD_SIZE_MB = int(os.environ.get("MAX_BUILD_SIZE_MB", "20"))
MAX_ASSET_SIZE_MB = int(os.environ.get("MAX_ASSET_SIZE_MB", "5"))


def setup_logging(verbose: bool) -> None:
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
    logger.addHandler(fh)
    if verbose:
        sh = logging.StreamHandler(sys.stderr)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)


class TestResult:
    def __init__(self, name: str, passed: bool, detail: str = ""):
        self.name = name
        self.passed = passed
        self.detail = detail

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        detail = f" ({self.detail})" if self.detail else ""
        return f"  [{status}] {self.name}{detail}"


# ---------------------------------------------------------------------------
# Test 1: Build output exists
# ---------------------------------------------------------------------------
def test_build_output(build_dir: Path) -> TestResult:
    """Check that index.html and sitemap.xml exist in the build directory."""
    if not build_dir.is_dir():
        return TestResult("Build output exists", False, f"directory not found: {build_dir}")

    index = build_dir / "index.html"
    sitemap = build_dir / "sitemap.xml"

    if not index.is_file():
        return TestResult("Build output exists", False, "index.html missing")

    detail = "index.html present"
    if sitemap.is_file():
        detail += ", sitemap.xml present"
    else:
        detail += ", sitemap.xml missing (warning)"

    return TestResult("Build output exists", True, detail)


# ---------------------------------------------------------------------------
# Test 2: Search index generated
# ---------------------------------------------------------------------------
def test_search_index(build_dir: Path, algolia_app_id: str, algolia_api_key: str,
                      algolia_index: str) -> TestResult:
    """Check local search index file or validate Algolia index."""
    # Check local search index
    search_files = list(build_dir.rglob("search-index*.json")) + \
                   list(build_dir.rglob("search-doc*.json")) + \
                   list(build_dir.rglob("lunr-index*.json"))

    if search_files:
        return TestResult("Search index generated", True,
                          f"local index: {search_files[0].name}")

    # Check Algolia
    if algolia_app_id and algolia_api_key and algolia_index:
        try:
            import requests
            url = f"https://{algolia_app_id}-dsn.algolia.net/1/indexes/{algolia_index}/query"
            headers = {
                "X-Algolia-Application-Id": algolia_app_id,
                "X-Algolia-API-Key": algolia_api_key,
                "Content-Type": "application/json",
            }
            resp = requests.post(url, json={"query": "", "hitsPerPage": 1},
                                 headers=headers, timeout=10)
            if resp.status_code == 200:
                hits = resp.json().get("nbHits", 0)
                return TestResult("Search index generated", True,
                                  f"Algolia index: {hits} hits")
            return TestResult("Search index generated", False,
                              f"Algolia returned status {resp.status_code}")
        except Exception as exc:
            return TestResult("Search index generated", False, f"Algolia error: {exc}")

    return TestResult("Search index generated", False, "no local index or Algolia config found")


# ---------------------------------------------------------------------------
# Test 3: API docs present
# ---------------------------------------------------------------------------
def test_api_docs(project_dir: Path) -> TestResult:
    """Check that docs/api/ contains .md files."""
    api_dir = project_dir / "docs" / "api"
    if not api_dir.is_dir():
        return TestResult("API docs present", False, "docs/api/ directory not found")

    md_files = list(api_dir.rglob("*.md"))
    if not md_files:
        return TestResult("API docs present", False, "no .md files in docs/api/")

    return TestResult("API docs present", True, f"{len(md_files)} files")


# ---------------------------------------------------------------------------
# Test 4: Skill docs present
# ---------------------------------------------------------------------------
def test_skill_docs(project_dir: Path) -> TestResult:
    """Check that docs/skills/ contains .md files."""
    skills_dir = project_dir / "docs" / "skills"
    if not skills_dir.is_dir():
        return TestResult("Skill docs present", False, "docs/skills/ directory not found")

    md_files = list(skills_dir.rglob("*.md"))
    if not md_files:
        return TestResult("Skill docs present", False, "no .md files in docs/skills/")

    return TestResult("Skill docs present", True, f"{len(md_files)} files")


# ---------------------------------------------------------------------------
# Test 5: Site accessible
# ---------------------------------------------------------------------------
def test_site_accessible(site_url: str) -> TestResult:
    """Check that the deployed site returns HTTP 200."""
    if not site_url:
        return TestResult("Site accessible", False, "no SITE_URL provided")

    try:
        import requests
        resp = requests.get(site_url, timeout=15, allow_redirects=True)
        if resp.status_code == 200:
            return TestResult("Site accessible", True, f"HTTP 200 at {site_url}")
        return TestResult("Site accessible", False,
                          f"HTTP {resp.status_code} at {site_url}")
    except ImportError:
        return TestResult("Site accessible", False, "requests library not installed")
    except Exception as exc:
        return TestResult("Site accessible", False, f"connection error: {exc}")


# ---------------------------------------------------------------------------
# Test 6: Internal links valid
# ---------------------------------------------------------------------------
def test_internal_links(build_dir: Path) -> TestResult:
    """Scan HTML files for broken internal links."""
    if not build_dir.is_dir():
        return TestResult("Internal links valid", False, "build directory not found")

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return TestResult("Internal links valid", False, "beautifulsoup4 not installed")

    html_files = list(build_dir.rglob("*.html"))
    if not html_files:
        return TestResult("Internal links valid", False, "no HTML files found")

    broken: list[str] = []
    checked = 0

    for html_file in html_files:
        try:
            content = html_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        soup = BeautifulSoup(content, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            # Only check internal links
            if href.startswith(("http://", "https://", "mailto:", "#", "javascript:")):
                continue

            # Resolve relative path
            target = (html_file.parent / href).resolve()
            # Handle directory index
            if target.is_dir():
                target = target / "index.html"
            elif not target.suffix:
                target = target.with_suffix(".html")
                if not target.is_file():
                    target = target.with_suffix("") / "index.html"

            checked += 1
            if not target.is_file():
                broken.append(f"{html_file.name} -> {href}")

    if broken:
        sample = broken[:5]
        return TestResult("Internal links valid", False,
                          f"{len(broken)} broken links (e.g. {sample[0]})")

    return TestResult("Internal links valid", True, f"{checked} links checked")


# ---------------------------------------------------------------------------
# Test 7: Performance metrics
# ---------------------------------------------------------------------------
def test_performance(build_dir: Path) -> TestResult:
    """Check build size and largest asset against thresholds."""
    if not build_dir.is_dir():
        return TestResult("Performance metrics", False, "build directory not found")

    # Calculate total build size
    total_bytes = sum(f.stat().st_size for f in build_dir.rglob("*") if f.is_file())
    total_mb = total_bytes / (1024 * 1024)

    # Find largest asset
    largest_bytes = 0
    largest_name = ""
    for f in build_dir.rglob("*"):
        if f.is_file():
            size = f.stat().st_size
            if size > largest_bytes:
                largest_bytes = size
                largest_name = f.name
    largest_mb = largest_bytes / (1024 * 1024)

    issues: list[str] = []
    if total_mb > MAX_BUILD_SIZE_MB:
        issues.append(f"build size {total_mb:.1f}MB > {MAX_BUILD_SIZE_MB}MB")
    if largest_mb > MAX_ASSET_SIZE_MB:
        issues.append(f"largest asset {largest_name} {largest_mb:.1f}MB > {MAX_ASSET_SIZE_MB}MB")

    if issues:
        return TestResult("Performance metrics", False, "; ".join(issues))

    return TestResult("Performance metrics", True,
                      f"build: {total_mb:.1f}MB, largest: {largest_name} ({largest_mb:.1f}MB)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Docusaurus deployment.")
    parser.add_argument("--project-dir", required=True, help="Docusaurus project directory")
    parser.add_argument("--build-dir", default="", help="Build output directory (default: PROJECT_DIR/build)")
    parser.add_argument("--site-url", default="", help="Deployed site URL for accessibility test")
    parser.add_argument("--algolia-app-id", default="", help="Algolia app ID")
    parser.add_argument("--algolia-api-key", default="", help="Algolia search API key")
    parser.add_argument("--algolia-index", default="", help="Algolia index name")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger.info("=== Deployment verification started ===")

    project_dir = Path(args.project_dir)
    build_dir = Path(args.build_dir) if args.build_dir else project_dir / "build"

    if not project_dir.is_dir():
        logger.error("Project directory not found: %s", args.project_dir)
        sys.exit(2)

    # Run all 7 tests
    results: list[TestResult] = [
        test_build_output(build_dir),
        test_search_index(build_dir, args.algolia_app_id, args.algolia_api_key, args.algolia_index),
        test_api_docs(project_dir),
        test_skill_docs(project_dir),
        test_site_accessible(args.site_url),
        test_internal_links(build_dir),
        test_performance(build_dir),
    ]

    # Report
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed

    for r in results:
        logger.info(str(r))

    logger.info("=== Verification complete: %d/%d passed ===", passed, len(results))

    # Output summary
    print(f"Verification: {passed}/{len(results)} tests passed")
    for r in results:
        print(str(r))

    if failed > 0:
        print(f"[WARN] {failed} test(s) failed")
        sys.exit(1)
    else:
        print(f"[OK] All {len(results)} verification tests passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
