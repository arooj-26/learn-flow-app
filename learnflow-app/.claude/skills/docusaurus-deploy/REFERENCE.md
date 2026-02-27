# Docusaurus Deploy - Technical Reference

Extended technical reference for the `docusaurus-deploy` skill. Covers architecture, configuration details, optimization strategies, and deployment target specifics.

## Docusaurus Project Architecture

```
docs-site/
├── docusaurus.config.js      # Main configuration
├── sidebars.js                # Sidebar navigation
├── package.json               # Dependencies
├── babel.config.js            # Babel configuration
├── src/
│   ├── css/
│   │   └── custom.css         # Custom theme CSS
│   ├── components/            # React components
│   └── pages/                 # Custom pages
│       └── index.js           # Landing page
├── docs/
│   ├── intro.md               # Getting started
│   ├── api/                   # Auto-generated API docs
│   │   ├── _category_.json
│   │   └── *.md
│   └── skills/                # Auto-generated skill docs
│       ├── _category_.json
│       ├── index.md
│       └── *.md
├── static/
│   └── img/                   # Static assets
├── blog/                      # Blog posts (optional)
├── i18n/                      # Translations (optional)
├── versioned_docs/            # Versioned docs (optional)
├── versioned_sidebars/        # Versioned sidebars (optional)
├── versions.json              # Version manifest (optional)
├── build/                     # Production build output
├── k8s/                       # Kubernetes manifests (K8s target)
├── vercel.json                # Vercel config (Vercel target)
├── netlify.toml               # Netlify config (Netlify target)
├── Dockerfile                 # Docker build (K8s target)
└── .github/
    └── workflows/
        └── deploy-docs.yml   # CI/CD workflow (optional)
```

## API Documentation Generation Pipeline

### TypeScript / JavaScript

The `generate_api_docs.py` script uses regex to extract JSDoc/TSDoc comment blocks:

```
Source file (.ts/.js/.tsx/.jsx)
    │
    ▼
Regex scan for /** ... */ blocks
    │
    ▼
Match preceding export/function/class/const declaration
    │
    ▼
Parse @param {type} name - description
Parse @returns {type} description
Parse @example code blocks
Parse other @tags
    │
    ▼
Generate Markdown with:
  - YAML front matter (title, sidebar_label, position, description)
  - Parameter table (Name | Type | Description)
  - Returns section
  - Code examples in fenced blocks
    │
    ▼
Write to docs/api/<module>/<symbol>.md
```

**Regex pattern** (simplified):
```
/\*\*\s*\n([\s\S]*?)\*/\s*\n\s*
(?:export\s+)?(?:default\s+)?
(?:(?:async\s+)?function\s+(\w+)|class\s+(\w+)|(?:const|let|var)\s+(\w+))
```

### Python

The `generate_api_docs.py` script uses the `ast` module for reliable parsing:

```
Source file (.py)
    │
    ▼
ast.parse() → Abstract Syntax Tree
    │
    ▼
ast.walk() → Find FunctionDef, AsyncFunctionDef, ClassDef nodes
    │
    ▼
ast.get_docstring() → Extract docstring
    │
    ▼
Detect format:
  - Google style:  "Args:", "Returns:", "Example:"
  - NumPy style:   Section headers underlined with "---"
  - Sphinx style:  ":param name:", ":returns:"
    │
    ▼
Parse into structured data (params, returns, examples)
    │
    ▼
Generate Markdown (same output format as TS/JS)
```

### Grouping Strategies

| Strategy | Output Structure | Best For |
|----------|-----------------|----------|
| `module` (default) | `docs/api/<parent-dir>/<symbol>.md` | Medium/large projects |
| `file` | `docs/api/<filename>/<symbol>.md` | Flat source structures |
| `flat` | `docs/api/<symbol>.md` | Small projects |

## Skill Documentation Generation Pipeline

```
.claude/skills/
    │
    ▼
Scan for SKILL.md files (recursive glob)
    │
    ▼
For each SKILL.md:
  ├── Parse YAML frontmatter (name, description, version)
  ├── Extract Markdown body
  ├── Check for REFERENCE.md (optional embed)
  └── List scripts/ directory contents
    │
    ▼
Generate:
  ├── docs/skills/index.md    (summary table of all skills)
  ├── docs/skills/<name>.md   (individual skill page)
  └── docs/skills/_category_.json (sidebar config)
```

## Search Configuration Reference

### Local Search (`@easyops-cn/docusaurus-search-local`)

Provides client-side full-text search with no external dependencies.

**Configuration in `docusaurus.config.js`:**
```javascript
themes: [
  [
    '@easyops-cn/docusaurus-search-local',
    {
      hashed: true,                          // Use hashed filenames
      language: ['en'],                      // Index language(s)
      highlightSearchTermsOnTargetPage: true, // Highlight matches
      explicitSearchResultPath: true,         // Show file paths
      docsRouteBasePath: '/docs',            // Docs route
      indexBlog: false,                      // Skip blog indexing
    },
  ],
],
```

**Generated files:** The build produces search index JSON files in the build output directory, used by the client-side search UI.

### Algolia DocSearch

Cloud-hosted search with crawling and relevance ranking.

**Configuration in `docusaurus.config.js`:**
```javascript
themeConfig: {
  algolia: {
    appId: 'YOUR_APP_ID',
    apiKey: 'YOUR_SEARCH_ONLY_API_KEY',  // Public search-only key
    indexName: 'YOUR_INDEX_NAME',
    contextualSearch: true,
    searchParameters: {},
    searchPagePath: 'search',
  },
},
```

**Validation:** The `configure_search.py` script validates credentials by making a test query to the Algolia API before writing configuration.

## Performance Optimization Reference

### Lazy Loading

The `@docusaurus/plugin-ideal-image` plugin provides:
- Responsive image generation (640px to 1030px, 2 steps)
- WebP format with JPEG fallback
- Lazy loading with blur-up placeholder
- Quality setting: 70 (configurable)

### Image Optimization

When `OPTIMIZE_IMAGES=1` is set during build:
- PNG/JPEG files are compressed using `sharp-cli` (if available)
- Quality target: 80%
- Applied to `build/img/` directory post-build

### PWA Support

When `ENABLE_PWA=true`:
- Service worker for offline access
- Installable as native app
- Activation strategies: `appInstalled`, `standalone`, `queryString`

### Caching Strategy

All deployment targets configure caching headers:

| Path | Cache-Control | TTL |
|------|--------------|-----|
| `/assets/*` | `public, max-age=31536000, immutable` | 1 year |
| `/*.html` | `public, max-age=0, must-revalidate` | None (always fresh) |
| `/sitemap.xml` | Default | Server default |

### Build Size Thresholds

| Metric | Threshold | Enforcement |
|--------|-----------|-------------|
| Total build size | 20 MB | `build_docs.sh` + `verify.py` |
| Largest single asset | 5 MB | `build_docs.sh` + `verify.py` |

## SEO Configuration

### Sitemap

Generated by `@docusaurus/plugin-sitemap`:
```javascript
sitemap: {
  changefreq: 'weekly',
  priority: 0.5,
  ignorePatterns: ['/tags/**'],
  filename: 'sitemap.xml',
}
```

### Open Graph

Configured via `themeConfig.metadata`:
```javascript
metadata: [
  { name: 'keywords', content: 'documentation, API' },
  { name: 'og:type', content: 'website' },
],
image: 'img/social-card.jpg',
```

### Structured Data

Docusaurus generates JSON-LD structured data for documentation pages automatically via the classic preset.

### Additional SEO Features

- `onBrokenLinks: 'throw'` — fails build on broken links
- `onBrokenMarkdownLinks: 'warn'` — warns on broken Markdown links
- Canonical URLs from `url` + `baseUrl` configuration
- Edit URL linking back to source on GitHub

## Versioning Reference

When `ENABLE_VERSIONING=true`, the init script sets up:

```
docs-site/
├── docs/                    # "Next" (unreleased) version
├── versioned_docs/
│   ├── version-1.0.0/      # Snapshot of docs at v1.0.0
│   └── version-2.0.0/      # Snapshot of docs at v2.0.0
├── versioned_sidebars/
│   ├── version-1.0.0-sidebars.json
│   └── version-2.0.0-sidebars.json
└── versions.json            # ["2.0.0", "1.0.0"]
```

**Creating a new version:**
```bash
cd docs-site
npx docusaurus docs:version 1.0.0
```

This snapshots `docs/` into `versioned_docs/version-1.0.0/` and adds `"1.0.0"` to `versions.json`.

## i18n Reference

When `ENABLE_I18N=true`, the init script configures:

```javascript
i18n: {
  defaultLocale: 'en',
  locales: ['en'],
}
```

**Adding a new locale:**
1. Add locale to `locales` array in `docusaurus.config.js`
2. Create translation files: `npx docusaurus write-translations --locale fr`
3. Translate files in `i18n/fr/`
4. Build with locale: `npx docusaurus build --locale fr`

**Directory structure:**
```
i18n/
├── fr/
│   ├── docusaurus-plugin-content-docs/
│   │   └── current/
│   │       └── intro.md    # Translated doc
│   └── docusaurus-theme-classic/
│       └── navbar.json      # Translated UI strings
```

## Analytics Integration

### Google Analytics (gtag)

When `GTAG_ID` is provided:
```javascript
plugins: [
  ['@docusaurus/plugin-google-gtag', {
    trackingID: 'G-XXXXXXXXXX',
    anonymizeIP: true,
  }],
],
```

### Plausible Analytics

To use Plausible instead, add to `docusaurus.config.js` manually:
```javascript
scripts: [
  {
    src: 'https://plausible.io/js/script.js',
    defer: true,
    'data-domain': 'yourdomain.com',
  },
],
```

## CI/CD GitHub Actions Workflow Reference

Generated by `deploy_docs.sh` when `GENERATE_CI=1`:

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main, master]
    paths:
      - 'docs/**'
      - 'src/**'
      - 'docusaurus.config.js'
      - 'sidebars.js'
      - 'package.json'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm
      - run: npm ci
      - run: npx docusaurus build
        env:
          NODE_ENV: production
      - uses: actions/upload-pages-artifact@v3
        with:
          path: build

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Trigger paths:** The workflow only runs when documentation-related files change, avoiding unnecessary builds for unrelated code changes.

## Deployment Target Architectures

### GitHub Pages

```
Local machine
    │
    ▼ npx docusaurus deploy
GitHub repo (gh-pages branch)
    │
    ▼ GitHub Pages serves
https://<org>.github.io/<repo>/
```

**Requirements:** Repository must have GitHub Pages enabled in Settings. The `gh-pages` branch is created automatically.

### Vercel

```
Local machine
    │
    ▼ vercel --prod
Vercel CDN (global edge network)
    │
    ▼ vercel.json routing
https://<project>.vercel.app
```

**Configuration (`vercel.json`):**
- Build command: `npx docusaurus build`
- Output directory: `build`
- Framework: `docusaurus-2`
- SPA rewrites for client-side routing
- Cache headers for static assets

### Netlify

```
Local machine
    │
    ▼ netlify deploy --prod
Netlify CDN (global edge network)
    │
    ▼ netlify.toml routing
https://<site>.netlify.app
```

**Configuration (`netlify.toml`):**
- Build command: `npx docusaurus build`
- Publish directory: `build`
- SPA redirects (200 rewrite)
- Cache headers for assets and HTML

### Kubernetes

```
Local machine
    │
    ▼ docker build (multi-stage)
┌─────────────────────────────┐
│ Stage 1: node:18-alpine     │
│   npm ci + npx docusaurus   │
│   build → /app/build        │
├─────────────────────────────┤
│ Stage 2: nginx:alpine       │
│   Copy build → nginx html   │
│   gzip + caching config     │
└─────────────────────────────┘
    │
    ▼ kubectl apply
┌─────────────────────────────┐
│ Kubernetes Cluster          │
│  ┌─────────────────────┐   │
│  │ Namespace: docs      │   │
│  │  ┌───────────────┐  │   │
│  │  │ Deployment    │  │   │
│  │  │ (2 replicas)  │  │   │
│  │  │  nginx:alpine │  │   │
│  │  └───────┬───────┘  │   │
│  │          │           │   │
│  │  ┌───────┴───────┐  │   │
│  │  │ Service       │  │   │
│  │  │ NodePort:30080│  │   │
│  │  └───────────────┘  │   │
│  └─────────────────────┘   │
└─────────────────────────────┘
```

**Kubernetes Resources:**

| Resource | Name | Key Config |
|----------|------|-----------|
| ConfigMap | `<image>-config` | NGINX_PORT |
| Deployment | `<image>` | 2 replicas, resource limits, health probes |
| Service | `<image>` | NodePort exposure |

**Resource limits:**
- CPU: 50m request / 200m limit
- Memory: 64Mi request / 128Mi limit

**Health probes:**
- Liveness: HTTP GET `/` every 10s (5s initial delay)
- Readiness: HTTP GET `/` every 5s (3s initial delay)

## Docker Build Strategy

Multi-stage build for minimal image size:

| Stage | Base Image | Purpose | Typical Size |
|-------|-----------|---------|-------------|
| Builder | `node:18-alpine` | Install deps + build | ~800MB |
| Runtime | `nginx:alpine` | Serve static files | ~25MB |

**nginx configuration:**
- `try_files` for SPA routing
- gzip compression for text types
- 1-year cache for `/assets/`

## Troubleshooting

### Build Errors

| Problem | Cause | Solution |
|---------|-------|---------|
| `Module not found` | Missing dependency | Run `npm install` in project dir |
| `Broken link` detected | Invalid internal href | Fix the link path in the source .md |
| Build size exceeds threshold | Too many/large assets | Optimize images, enable lazy loading |
| `SyntaxError` in config | Invalid docusaurus.config.js | Check JS syntax, validate with Node REPL |

### Deployment Errors

| Problem | Cause | Solution |
|---------|-------|---------|
| GitHub Pages 404 | Pages not enabled | Enable in repo Settings → Pages |
| Vercel auth error | Invalid/expired token | Regenerate `VERCEL_TOKEN` |
| Netlify build fail | Wrong build command | Check `netlify.toml` build settings |
| K8s ImagePullBackOff | Image not in registry | Push image or use local registry |
| K8s pod CrashLoopBackOff | nginx config error | Check pod logs with `kubectl logs` |

### Search Issues

| Problem | Cause | Solution |
|---------|-------|---------|
| No search results | Index not generated | Rebuild and check for search index files |
| Algolia empty index | Crawler not configured | Set up Algolia DocSearch crawler |
| Local search slow | Large index | Reduce indexed content scope |

### Generation Errors

| Problem | Cause | Solution |
|---------|-------|---------|
| No symbols found | No JSDoc/docstrings | Add documentation comments to source |
| Parse errors in Python | Invalid syntax | Fix syntax errors in source files |
| Missing skill docs | No SKILL.md files | Create SKILL.md with YAML frontmatter |

## Integration with Other Skills

### nextjs-k8s-deploy

Generate API docs for React components and hooks:
```bash
python generate_api_docs.py \
  --source-dirs ../frontend/src/components ../frontend/src/hooks \
  --output-dir docs-site/docs/api \
  --languages typescript
```

### kafka-k8s-setup

Document Kafka topic schemas by scanning topic configuration:
```bash
python generate_api_docs.py \
  --source-dirs ../kafka-config/schemas \
  --output-dir docs-site/docs/api/events \
  --languages typescript
```

### postgres-k8s-setup

Document database migrations:
```bash
python generate_skill_docs.py \
  --skills-dir .claude/skills \
  --output-dir docs-site/docs/skills \
  --include-scripts --include-reference
```

Migration SQL files can be referenced from the skill documentation pages.

### fastapi-dapr-agent

Document FastAPI endpoints (docstrings on route handlers):
```bash
python generate_api_docs.py \
  --source-dirs ../services/api \
  --output-dir docs-site/docs/api/endpoints \
  --languages python
```

### agents-md-gen

The `agents-md-gen` skill produces a single `AGENTS.md` file. This skill complements it by generating a full browsable documentation site with navigation, search, and cross-references.
