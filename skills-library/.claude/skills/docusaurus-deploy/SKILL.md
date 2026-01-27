---
name: docusaurus-deploy
description: "Deploy production-grade Docusaurus documentation sites with auto-generated API docs, search integration, and multi-target deployment (GitHub Pages, Vercel, Netlify, Kubernetes)."
version: 1.0.0
allowed-tools:
  - Bash(npm*)
  - Bash(npx*)
  - Bash(node*)
  - Bash(kubectl*)
  - Bash(docker*)
  - Bash(python*)
  - Bash(bash*)
  - Bash(curl*)
  - Bash(pip*)
  - Bash(gh*)
  - Read
  - Write
---

# docusaurus-deploy

Deploy production-grade Docusaurus documentation sites with auto-generated API documentation from source code comments, full-text search integration, SEO optimization, and multi-target deployment support.

## When to Use

Use this skill when:
- You need a browsable documentation site for a project or organization
- You want API reference docs auto-generated from JSDoc/TSDoc/Python docstrings
- You want to document a skills library with auto-generated pages
- You need full-text search (local or Algolia) in your docs
- You need to deploy docs to GitHub Pages, Vercel, Netlify, or Kubernetes
- You want CI/CD automation for documentation updates

## Prerequisites

| Prerequisite | Version | Required For |
|-------------|---------|--------------|
| Node.js | 18+ | All steps |
| npm | 9+ | All steps |
| Python | 3.9+ | Steps 2-4, 7 |
| pip | latest | Python deps |
| Docker | 20+ | K8s deployment |
| kubectl | 1.25+ | K8s deployment |
| git | 2.0+ | GitHub Pages |
| vercel CLI | latest | Vercel deployment |
| netlify CLI | latest | Netlify deployment |
| gh CLI | latest | GitHub Pages (fallback) |

## Instructions

### Step 1: Initialize Docusaurus Project

```bash
pip install -r .claude/skills/docusaurus-deploy/scripts/requirements.txt
bash .claude/skills/docusaurus-deploy/scripts/init_docusaurus.sh
```

#### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PROJECT_NAME` | `docs-site` | Project directory name |
| `SITE_TITLE` | `Documentation` | Site title in navbar and metadata |
| `SITE_URL` | `https://example.com` | Canonical site URL |
| `ORG_NAME` | `my-org` | GitHub organization name |
| `REPO_NAME` | `my-repo` | GitHub repository name |
| `ENABLE_BLOG` | `false` | Enable blog section |
| `THEME_COLOR` | `#2e8555` | Primary theme color |
| `LOCALE` | `en` | Default locale |
| `GTAG_ID` | *(empty)* | Google Analytics tracking ID |
| `BASE_URL` | `/` | Base URL path |
| `ENABLE_VERSIONING` | `false` | Enable docs versioning infrastructure |
| `ENABLE_I18N` | `false` | Enable i18n infrastructure |
| `ENABLE_PWA` | `false` | Enable Progressive Web App support |

### Step 2: Generate API Docs from Source Code

```bash
python .claude/skills/docusaurus-deploy/scripts/generate_api_docs.py \
  --source-dirs src/ lib/ \
  --output-dir docs-site/docs/api \
  --languages typescript javascript python
```

Parses JSDoc/TSDoc comment blocks (regex-based) and Python docstrings (`ast` module — Google, NumPy, and Sphinx formats). Generates Markdown with Docusaurus front matter, parameter tables, and code examples.

#### Flags

| Flag | Description |
|------|-------------|
| `--source-dirs` | Directories to scan (required, space-separated) |
| `--output-dir` | Output directory for Markdown files (required) |
| `--languages` | Languages to parse (default: typescript javascript python) |
| `--include-private` | Include private/underscore-prefixed symbols |
| `--group-by` | Grouping strategy: `file`, `module`, `flat` (default: module) |
| `--dry-run` | Print what would be generated without writing files |
| `--verbose` | Verbose logging to stderr |

### Step 3: Generate Skill Library Docs

```bash
python .claude/skills/docusaurus-deploy/scripts/generate_skill_docs.py \
  --skills-dir .claude/skills \
  --output-dir docs-site/docs/skills \
  --include-scripts \
  --include-reference
```

Scans for SKILL.md files, parses YAML frontmatter, and generates an index page with a summary table and individual skill pages.

#### Flags

| Flag | Description |
|------|-------------|
| `--skills-dir` | Root skills directory (required) |
| `--output-dir` | Output directory for Markdown files (required) |
| `--include-scripts` | Include script listings in skill pages |
| `--include-reference` | Embed REFERENCE.md content in skill pages |
| `--verbose` | Verbose logging to stderr |

### Step 4: Configure Search

```bash
# Local search (default)
python .claude/skills/docusaurus-deploy/scripts/configure_search.py \
  --project-dir docs-site \
  --provider local

# Algolia search
python .claude/skills/docusaurus-deploy/scripts/configure_search.py \
  --project-dir docs-site \
  --provider algolia \
  --algolia-app-id YOUR_APP_ID \
  --algolia-api-key YOUR_SEARCH_KEY \
  --algolia-index YOUR_INDEX_NAME
```

Idempotent — detects existing configuration and updates in place.

#### Flags

| Flag | Description |
|------|-------------|
| `--project-dir` | Docusaurus project directory (required) |
| `--provider` | Search provider: `local` or `algolia` (default: local) |
| `--algolia-app-id` | Algolia application ID |
| `--algolia-api-key` | Algolia search-only API key |
| `--algolia-index` | Algolia index name |
| `--verbose` | Verbose logging to stderr |

### Step 5: Build Documentation

```bash
bash .claude/skills/docusaurus-deploy/scripts/build_docs.sh
```

Cleans previous build, runs `npx docusaurus build`, and validates output (index.html, sitemap.xml, size thresholds).

#### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PROJECT_DIR` | `.` | Docusaurus project directory |
| `BASE_URL` | `/` | Base URL for the build |
| `ANALYZE_BUNDLE` | `0` | Set to `1` for bundle analysis |
| `ENABLE_PWA` | `false` | Enable PWA in build |
| `OPTIMIZE_IMAGES` | `0` | Set to `1` for image optimization |
| `NODE_ENV` | `production` | Node environment |
| `MAX_BUILD_SIZE_MB` | `20` | Maximum build size threshold |
| `MAX_ASSET_SIZE_MB` | `5` | Maximum single asset size threshold |

### Step 6: Deploy Documentation

```bash
# GitHub Pages (default)
DEPLOY_TARGET=github-pages bash .claude/skills/docusaurus-deploy/scripts/deploy_docs.sh

# Vercel
DEPLOY_TARGET=vercel VERCEL_TOKEN=xxx bash .claude/skills/docusaurus-deploy/scripts/deploy_docs.sh

# Netlify
DEPLOY_TARGET=netlify NETLIFY_TOKEN=xxx bash .claude/skills/docusaurus-deploy/scripts/deploy_docs.sh

# Kubernetes
DEPLOY_TARGET=k8s NAMESPACE=docs IMAGE_NAME=docs-site bash .claude/skills/docusaurus-deploy/scripts/deploy_docs.sh
```

Set `GENERATE_CI=1` to also generate a `.github/workflows/deploy-docs.yml` workflow.

#### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPLOY_TARGET` | `github-pages` | Target: `github-pages`, `vercel`, `netlify`, `k8s` |
| `PROJECT_DIR` | `.` | Docusaurus project directory |
| `MAX_RETRIES` | `3` | Maximum deployment retry attempts |
| `RETRY_BACKOFF` | `5` | Base retry backoff in seconds |
| `GENERATE_CI` | `0` | Set to `1` to generate CI/CD workflow |
| `GH_PAGES_BRANCH` | `gh-pages` | GitHub Pages branch |
| `GIT_USER` | *(empty)* | Git user for GitHub Pages deploy |
| `VERCEL_TOKEN` | *(empty)* | Vercel deployment token |
| `NETLIFY_TOKEN` | *(empty)* | Netlify auth token |
| `NETLIFY_SITE_ID` | *(empty)* | Netlify site ID |
| `NAMESPACE` | `docs` | Kubernetes namespace |
| `IMAGE_NAME` | `docs-site` | Docker image name |
| `IMAGE_TAG` | `latest` | Docker image tag |
| `REGISTRY` | *(empty)* | Docker registry (e.g., `ghcr.io/org`) |
| `REPLICAS` | `2` | Kubernetes replica count |
| `NODE_PORT` | `30080` | Kubernetes NodePort |

### Step 7: Verify Deployment

```bash
python .claude/skills/docusaurus-deploy/scripts/verify.py \
  --project-dir docs-site \
  --site-url https://example.com
```

Runs 7 verification tests: build output, search index, API docs, skill docs, site accessibility, internal links, and performance metrics.

#### Flags

| Flag | Description |
|------|-------------|
| `--project-dir` | Docusaurus project directory (required) |
| `--build-dir` | Build output directory (default: PROJECT_DIR/build) |
| `--site-url` | Deployed site URL for accessibility test |
| `--algolia-app-id` | Algolia app ID for search validation |
| `--algolia-api-key` | Algolia API key for search validation |
| `--algolia-index` | Algolia index name for search validation |
| `--verbose` | Verbose logging to stderr |

### Step 8: Cleanup

```bash
# Interactive cleanup
bash .claude/skills/docusaurus-deploy/scripts/cleanup.sh --target github-pages

# Force cleanup (no confirmation)
bash .claude/skills/docusaurus-deploy/scripts/cleanup.sh --target k8s --force --delete-namespace

# Keep content, remove only deployment artifacts
bash .claude/skills/docusaurus-deploy/scripts/cleanup.sh --target vercel --keep-content --force
```

#### Flags

| Flag | Description |
|------|-------------|
| `--target` | Deployment target to clean up |
| `--force` | Skip confirmation prompt |
| `--keep-content` | Only remove deployment artifacts, keep docs content |
| `--delete-namespace` | Also delete K8s namespace |
| `--project-dir` | Docusaurus project directory |
| `--namespace` | K8s namespace to clean up |
| `--verbose` | Verbose logging to stderr |

## Documentation Generation Specifications

### API Documentation Pipeline

| Source | Parser | Input | Output |
|--------|--------|-------|--------|
| TypeScript/JavaScript | Regex JSDoc `/** */` | `@param`, `@returns`, `@example` | Markdown with param tables |
| Python | `ast` module | Google, NumPy, Sphinx docstrings | Markdown with param tables |

Each generated file includes:
- Docusaurus YAML front matter (title, sidebar_label, sidebar_position, description)
- Function/class name, kind, language, source file
- Parameter table (Name, Type, Description)
- Return type documentation
- Code examples in fenced blocks
- `_category_.json` for sidebar organization

### Skill Documentation Pipeline

| Input | Parser | Output |
|-------|--------|--------|
| `SKILL.md` files | YAML frontmatter + Markdown body | Individual skill pages |
| `REFERENCE.md` files | Markdown body (optional embed) | Appended to skill pages |
| Scripts directory | File listing | Script tables in skill pages |
| All skills | Aggregation | Index page with summary table |

## Validation Checklist

- [ ] Docusaurus project scaffolded with `classic` preset
- [ ] Plugins installed: ideal-image, search-local, sitemap
- [ ] `docusaurus.config.js` configured with SEO, navbar, footer, prism
- [ ] Custom CSS set with theme color variables
- [ ] Sidebars configured for docs, API, and skills sections
- [ ] API docs generated from source code with front matter
- [ ] Skill docs generated with index table and individual pages
- [ ] Search configured (local or Algolia)
- [ ] Build passes with no broken links or markdown warnings
- [ ] Build size within thresholds (< 20MB total, < 5MB per asset)
- [ ] Deployment successful to target platform
- [ ] Site returns HTTP 200
- [ ] All 7 verification tests pass

## Success Criteria

```
[OK] Docusaurus initialized (project: docs-site, plugins: search-local, ideal-image, sitemap)
[OK] API docs generated (files: 42, symbols: 128)
[OK] Skill docs generated (skills: 6, files: 7)
[OK] Search configured (provider: local)
[OK] Documentation built (dir: docs-site/build, size: 4520KB)
[OK] Documentation deployed (target: github-pages)
[OK] All 7 verification tests passed
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Fatal error |
| 2 | Prerequisites not met / no source files |
| 3 | Build validation / deployment / cleanup failed |
| 4 | Configuration error / user cancelled |

## Timing Specifications

All scripts log timestamps to the log file. No inline timing estimates are provided — completion depends on project size, network conditions, and deployment target.

## Token Efficiency

- All heavy operations run in external scripts (bash/python)
- Scripts output a single `[OK]` or `[ERROR]` summary line to stdout
- Detailed logs go to `.docusaurus-deploy.log`, not stdout
- `--verbose` flag enables stderr logging for debugging
- `--dry-run` flag (where available) previews without writing

## Integration Requirements

This skill integrates with existing skills in the library:

| Skill | Integration |
|-------|-------------|
| `nextjs-k8s-deploy` | Document React components and hooks from `src/` |
| `kafka-k8s-setup` | Document event topic schemas |
| `postgres-k8s-setup` | Document database schema and migrations |
| `fastapi-dapr-agent` | Document FastAPI endpoints and Dapr services |
| `agents-md-gen` | Complement AGENTS.md with a full browsable docs site |
