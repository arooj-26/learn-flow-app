#!/usr/bin/env python3
"""configure_search.py - Configure search for a Docusaurus site.

Supports two providers:
  - local: Installs and configures @easyops-cn/docusaurus-search-local
  - algolia: Validates Algolia credentials via API and configures themeConfig.algolia

Idempotent: detects existing configuration and updates in place.

Exit codes:
    0 - Success
    1 - Fatal error
    2 - Project directory not found
    3 - Algolia credentials invalid
"""

import argparse
import io
import json
import logging
import os
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

LOG_FILE = os.environ.get("LOG_FILE", ".docusaurus-deploy.log")
logger = logging.getLogger("configure_search")


def setup_logging(verbose: bool) -> None:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
    logger.addHandler(file_handler)
    if verbose:
        sh = logging.StreamHandler(sys.stderr)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)


# ---------------------------------------------------------------------------
# Local search configuration
# ---------------------------------------------------------------------------

LOCAL_SEARCH_THEME_BLOCK = """\
    [
      '@easyops-cn/docusaurus-search-local',
      /** @type {import("@easyops-cn/docusaurus-search-local").PluginOptions} */
      ({
        hashed: true,
        language: ['en'],
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
        docsRouteBasePath: '/docs',
        indexBlog: false,
      }),
    ],"""


def configure_local_search(project_dir: Path) -> None:
    """Install and configure local search plugin."""
    config_file = project_dir / "docusaurus.config.js"
    if not config_file.is_file():
        logger.error("docusaurus.config.js not found in %s", project_dir)
        sys.exit(2)

    content = config_file.read_text(encoding="utf-8", errors="replace")

    # Check if already configured
    if "@easyops-cn/docusaurus-search-local" in content:
        logger.info("Local search already configured – skipping")
        return

    # Insert into themes array if it exists
    if "themes:" in content:
        # Append to existing themes
        content = content.replace(
            "themes: [",
            "themes: [\n" + LOCAL_SEARCH_THEME_BLOCK,
            1,
        )
    else:
        # Add themes section before themeConfig
        content = content.replace(
            "themeConfig:",
            "themes: [\n" + LOCAL_SEARCH_THEME_BLOCK + "\n  ],\n\n  themeConfig:",
            1,
        )

    config_file.write_text(content, encoding="utf-8")
    logger.info("Local search configured in docusaurus.config.js")

    # Install npm package
    logger.info("Installing @easyops-cn/docusaurus-search-local...")
    ret = os.system(f'cd "{project_dir}" && npm install --save @easyops-cn/docusaurus-search-local')
    if ret != 0:
        logger.error("npm install failed for search-local plugin")
        sys.exit(1)

    logger.info("Local search plugin installed")


# ---------------------------------------------------------------------------
# Algolia search configuration
# ---------------------------------------------------------------------------

def validate_algolia_credentials(app_id: str, api_key: str, index_name: str) -> bool:
    """Validate Algolia credentials by querying the API."""
    try:
        import requests
    except ImportError:
        logger.warning("requests not installed – skipping Algolia validation")
        return True

    url = f"https://{app_id}-dsn.algolia.net/1/indexes/{index_name}/query"
    headers = {
        "X-Algolia-Application-Id": app_id,
        "X-Algolia-API-Key": api_key,
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(url, json={"query": "test", "hitsPerPage": 1},
                             headers=headers, timeout=10)
        if resp.status_code == 200:
            logger.info("Algolia credentials valid")
            return True
        logger.error("Algolia returned status %d: %s", resp.status_code, resp.text[:200])
        return False
    except requests.RequestException as exc:
        logger.error("Algolia API request failed: %s", exc)
        return False


ALGOLIA_CONFIG_BLOCK = """\
      algolia: {{
        appId: '{app_id}',
        apiKey: '{api_key}',
        indexName: '{index_name}',
        contextualSearch: true,
        searchParameters: {{}},
        searchPagePath: 'search',
      }},"""


def configure_algolia_search(project_dir: Path, app_id: str, api_key: str,
                             index_name: str) -> None:
    """Configure Algolia DocSearch in docusaurus.config.js."""
    if not app_id or not api_key or not index_name:
        logger.error("Algolia requires --algolia-app-id, --algolia-api-key, and --algolia-index")
        sys.exit(3)

    if not validate_algolia_credentials(app_id, api_key, index_name):
        logger.error("Algolia credential validation failed")
        sys.exit(3)

    config_file = project_dir / "docusaurus.config.js"
    if not config_file.is_file():
        logger.error("docusaurus.config.js not found in %s", project_dir)
        sys.exit(2)

    content = config_file.read_text(encoding="utf-8", errors="replace")

    block = ALGOLIA_CONFIG_BLOCK.format(
        app_id=app_id, api_key=api_key, index_name=index_name
    )

    # Check if already configured
    if "algolia:" in content:
        # Replace existing algolia config
        content = re.sub(
            r"algolia:\s*\{[^}]+\},?",
            block.strip(),
            content,
            count=1,
        )
        logger.info("Updated existing Algolia configuration")
    else:
        # Insert into themeConfig
        content = content.replace(
            "themeConfig:",
            "themeConfig:\n    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */\n    ({" + block,
            1,
        ) if "themeConfig:\n" in content else content.replace(
            "themeConfig:",
            "themeConfig:" + block,
            1,
        )
        logger.info("Added Algolia configuration to themeConfig")

    # Remove local search if switching to Algolia
    if "@easyops-cn/docusaurus-search-local" in content:
        logger.info("Removing local search plugin (switching to Algolia)")
        content = re.sub(
            r"\[\s*'@easyops-cn/docusaurus-search-local'[\s\S]*?\],?\s*",
            "",
            content,
        )

    config_file.write_text(content, encoding="utf-8")
    logger.info("Algolia search configured")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Configure search for Docusaurus.")
    parser.add_argument("--project-dir", required=True, help="Docusaurus project directory")
    parser.add_argument("--provider", choices=["local", "algolia"], default="local",
                        help="Search provider (default: local)")
    parser.add_argument("--algolia-app-id", default="", help="Algolia application ID")
    parser.add_argument("--algolia-api-key", default="", help="Algolia search API key")
    parser.add_argument("--algolia-index", default="", help="Algolia index name")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger.info("=== Search configuration started (provider: %s) ===", args.provider)

    project_dir = Path(args.project_dir)
    if not project_dir.is_dir():
        logger.error("Project directory does not exist: %s", args.project_dir)
        sys.exit(2)

    if args.provider == "local":
        configure_local_search(project_dir)
    else:
        configure_algolia_search(
            project_dir,
            args.algolia_app_id,
            args.algolia_api_key,
            args.algolia_index,
        )

    logger.info("=== Search configuration complete ===")
    print(f"[OK] Search configured (provider: {args.provider})")


if __name__ == "__main__":
    main()
