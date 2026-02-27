#!/usr/bin/env bash
# init_docusaurus.sh - Initialize a Docusaurus documentation site with production-grade configuration.
#
# Validates prerequisites, scaffolds a Docusaurus project with the classic preset,
# installs plugins (ideal-image, search-local, sitemap, PWA, gtag), configures
# custom CSS, sidebar, versioning/i18n infrastructure, and SEO defaults.
#
# Exit codes:
#   0 - Success
#   1 - Fatal error
#   2 - Prerequisites not met

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration (override via environment variables)
# ---------------------------------------------------------------------------
PROJECT_NAME="${PROJECT_NAME:-docs-site}"
SITE_TITLE="${SITE_TITLE:-Documentation}"
SITE_URL="${SITE_URL:-https://example.com}"
ORG_NAME="${ORG_NAME:-my-org}"
REPO_NAME="${REPO_NAME:-my-repo}"
ENABLE_BLOG="${ENABLE_BLOG:-false}"
THEME_COLOR="${THEME_COLOR:-#2e8555}"
LOCALE="${LOCALE:-en}"
GTAG_ID="${GTAG_ID:-}"
BASE_URL="${BASE_URL:-/}"
OUTPUT_DIR="${OUTPUT_DIR:-.}"
ENABLE_VERSIONING="${ENABLE_VERSIONING:-false}"
ENABLE_I18N="${ENABLE_I18N:-false}"
ENABLE_PWA="${ENABLE_PWA:-false}"

LOG_FILE="${LOG_FILE:-.docusaurus-deploy.log}"
VERBOSE="${VERBOSE:-0}"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
log() {
    local level="$1"; shift
    local msg="$*"
    local ts
    ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")"
    echo "[$ts] [$level] $msg" >> "$LOG_FILE"
    if [[ "$VERBOSE" == "1" ]] || [[ "$level" == "ERROR" ]]; then
        echo "[$level] $msg" >&2
    fi
}

# ---------------------------------------------------------------------------
# Cleanup trap
# ---------------------------------------------------------------------------
cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        log "ERROR" "init_docusaurus.sh failed with exit code $exit_code"
    fi
}
trap cleanup EXIT

# ---------------------------------------------------------------------------
# Prerequisite validation
# ---------------------------------------------------------------------------
validate_prerequisites() {
    log "INFO" "Validating prerequisites..."

    if ! command -v node &>/dev/null; then
        log "ERROR" "Node.js is not installed"
        exit 2
    fi

    local node_major
    node_major="$(node -v | sed 's/v//' | cut -d. -f1)"
    if [[ "$node_major" -lt 18 ]]; then
        log "ERROR" "Node.js 18+ required (found v$(node -v))"
        exit 2
    fi

    if ! command -v npm &>/dev/null; then
        log "ERROR" "npm is not installed"
        exit 2
    fi

    local npm_major
    npm_major="$(npm -v | cut -d. -f1)"
    if [[ "$npm_major" -lt 9 ]]; then
        log "ERROR" "npm 9+ required (found $(npm -v))"
        exit 2
    fi

    if ! command -v npx &>/dev/null; then
        log "ERROR" "npx is not installed"
        exit 2
    fi

    log "INFO" "Prerequisites OK (node $(node -v), npm $(npm -v))"
}

# ---------------------------------------------------------------------------
# Scaffold Docusaurus project
# ---------------------------------------------------------------------------
scaffold_project() {
    local project_dir="${OUTPUT_DIR}/${PROJECT_NAME}"

    if [[ -d "$project_dir" ]] && [[ -f "$project_dir/docusaurus.config.js" ]]; then
        log "INFO" "Docusaurus project already exists at $project_dir – skipping scaffold"
        return 0
    fi

    log "INFO" "Scaffolding Docusaurus project: $PROJECT_NAME"
    cd "$OUTPUT_DIR"
    npx create-docusaurus@latest "$PROJECT_NAME" classic --javascript >> "$LOG_FILE" 2>&1
    cd - >/dev/null
    log "INFO" "Scaffold complete"
}

# ---------------------------------------------------------------------------
# Install plugins
# ---------------------------------------------------------------------------
install_plugins() {
    local project_dir="${OUTPUT_DIR}/${PROJECT_NAME}"
    cd "$project_dir"

    log "INFO" "Installing Docusaurus plugins..."

    local plugins=(
        "@docusaurus/plugin-ideal-image"
        "@easyops-cn/docusaurus-search-local"
        "@docusaurus/plugin-sitemap"
    )

    if [[ "$ENABLE_PWA" == "true" ]]; then
        plugins+=("@docusaurus/plugin-pwa")
    fi

    if [[ -n "$GTAG_ID" ]]; then
        plugins+=("@docusaurus/plugin-google-gtag")
    fi

    npm install --save "${plugins[@]}" >> "$LOG_FILE" 2>&1

    cd - >/dev/null
    log "INFO" "Plugins installed"
}

# ---------------------------------------------------------------------------
# Generate docusaurus.config.js
# ---------------------------------------------------------------------------
generate_config() {
    local project_dir="${OUTPUT_DIR}/${PROJECT_NAME}"
    local config_file="$project_dir/docusaurus.config.js"

    log "INFO" "Generating docusaurus.config.js..."

    local blog_config="false"
    if [[ "$ENABLE_BLOG" == "true" ]]; then
        blog_config='{
          showReadingTime: true,
          editUrl: "https://github.com/'"$ORG_NAME"'/'"$REPO_NAME"'/tree/main/",
        }'
    fi

    local i18n_config=""
    if [[ "$ENABLE_I18N" == "true" ]]; then
        i18n_config="
  i18n: {
    defaultLocale: '${LOCALE}',
    locales: ['${LOCALE}'],
  },"
    fi

    local gtag_plugin=""
    if [[ -n "$GTAG_ID" ]]; then
        gtag_plugin="
      [
        '@docusaurus/plugin-google-gtag',
        {
          trackingID: '${GTAG_ID}',
          anonymizeIP: true,
        },
      ],"
    fi

    local pwa_plugin=""
    if [[ "$ENABLE_PWA" == "true" ]]; then
        pwa_plugin="
      [
        '@docusaurus/plugin-pwa',
        {
          debug: false,
          offlineModeActivationStrategies: ['appInstalled', 'standalone', 'queryString'],
          pwaHead: [
            { tagName: 'link', rel: 'icon', href: '/img/logo.png' },
            { tagName: 'link', rel: 'manifest', href: '/manifest.json' },
            { tagName: 'meta', name: 'theme-color', content: '${THEME_COLOR}' },
          ],
        },
      ],"
    fi

    cat > "$config_file" << CONFIGEOF
// @ts-check

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: '${SITE_TITLE}',
  tagline: 'Production-grade documentation',
  favicon: 'img/favicon.ico',

  url: '${SITE_URL}',
  baseUrl: '${BASE_URL}',

  organizationName: '${ORG_NAME}',
  projectName: '${REPO_NAME}',
${i18n_config}
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/${ORG_NAME}/${REPO_NAME}/tree/main/',
        },
        blog: ${blog_config},
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
          ignorePatterns: ['/tags/**'],
          filename: 'sitemap.xml',
        },
      }),
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-ideal-image',
      {
        quality: 70,
        max: 1030,
        min: 640,
        steps: 2,
        disableInDev: false,
      },
    ],${gtag_plugin}${pwa_plugin}
  ],

  themes: [
    [
      '@easyops-cn/docusaurus-search-local',
      /** @type {import("@easyops-cn/docusaurus-search-local").PluginOptions} */
      ({
        hashed: true,
        language: ['${LOCALE}'],
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/social-card.jpg',
      navbar: {
        title: '${SITE_TITLE}',
        logo: {
          alt: '${SITE_TITLE} Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Docs',
          },
          {
            type: 'docSidebar',
            sidebarId: 'apiSidebar',
            position: 'left',
            label: 'API',
          },
          {
            href: 'https://github.com/${ORG_NAME}/${REPO_NAME}',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              { label: 'Getting Started', to: '/docs/intro' },
              { label: 'API Reference', to: '/docs/api/' },
            ],
          },
          {
            title: 'Community',
            items: [
              { label: 'GitHub', href: 'https://github.com/${ORG_NAME}/${REPO_NAME}' },
            ],
          },
        ],
        copyright: 'Copyright \u00a9 ' + new Date().getFullYear() + ' ${ORG_NAME}. Built with Docusaurus.',
      },
      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.dracula,
        additionalLanguages: ['bash', 'python', 'json', 'yaml', 'docker', 'toml'],
      },
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      metadata: [
        { name: 'keywords', content: '${SITE_TITLE}, documentation, API' },
        { name: 'og:type', content: 'website' },
      ],
    }),
};

module.exports = config;
CONFIGEOF

    log "INFO" "docusaurus.config.js generated"
}

# ---------------------------------------------------------------------------
# Configure custom CSS
# ---------------------------------------------------------------------------
configure_custom_css() {
    local css_file="${OUTPUT_DIR}/${PROJECT_NAME}/src/css/custom.css"

    log "INFO" "Writing custom CSS..."

    cat > "$css_file" << 'CSSEOF'
:root {
  --ifm-color-primary: THEME_COLOR_PLACEHOLDER;
  --ifm-color-primary-dark: color-mix(in srgb, var(--ifm-color-primary) 85%, black);
  --ifm-color-primary-darker: color-mix(in srgb, var(--ifm-color-primary) 75%, black);
  --ifm-color-primary-darkest: color-mix(in srgb, var(--ifm-color-primary) 60%, black);
  --ifm-color-primary-light: color-mix(in srgb, var(--ifm-color-primary) 85%, white);
  --ifm-color-primary-lighter: color-mix(in srgb, var(--ifm-color-primary) 75%, white);
  --ifm-color-primary-lightest: color-mix(in srgb, var(--ifm-color-primary) 60%, white);
  --ifm-code-font-size: 95%;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.1);
}

[data-theme='dark'] {
  --ifm-color-primary: THEME_COLOR_PLACEHOLDER;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.3);
}

.hero {
  text-align: center;
}

.footer--dark {
  --ifm-footer-background-color: #1b1b1d;
}
CSSEOF

    # Replace placeholder with actual color
    if command -v sed &>/dev/null; then
        sed -i "s/THEME_COLOR_PLACEHOLDER/${THEME_COLOR}/g" "$css_file" 2>/dev/null || \
        sed "s/THEME_COLOR_PLACEHOLDER/${THEME_COLOR}/g" "$css_file" > "${css_file}.tmp" && mv "${css_file}.tmp" "$css_file"
    fi

    log "INFO" "Custom CSS configured"
}

# ---------------------------------------------------------------------------
# Configure sidebars
# ---------------------------------------------------------------------------
configure_sidebars() {
    local sidebars_file="${OUTPUT_DIR}/${PROJECT_NAME}/sidebars.js"

    log "INFO" "Writing sidebars.js..."

    cat > "$sidebars_file" << 'SIDEBAREOF'
/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: ['intro'],
      collapsed: false,
    },
  ],
  apiSidebar: [
    {
      type: 'autogenerated',
      dirName: 'api',
    },
  ],
  skillsSidebar: [
    {
      type: 'autogenerated',
      dirName: 'skills',
    },
  ],
};

module.exports = sidebars;
SIDEBAREOF

    log "INFO" "Sidebars configured"
}

# ---------------------------------------------------------------------------
# Set up directory structure for docs
# ---------------------------------------------------------------------------
setup_docs_dirs() {
    local docs_dir="${OUTPUT_DIR}/${PROJECT_NAME}/docs"

    log "INFO" "Setting up docs directory structure..."

    mkdir -p "$docs_dir/api"
    mkdir -p "$docs_dir/skills"

    # Create placeholder API category
    if [[ ! -f "$docs_dir/api/_category_.json" ]]; then
        cat > "$docs_dir/api/_category_.json" << 'EOF'
{
  "label": "API Reference",
  "position": 2,
  "link": {
    "type": "generated-index",
    "description": "Auto-generated API documentation from source code."
  }
}
EOF
    fi

    # Create placeholder skills category
    if [[ ! -f "$docs_dir/skills/_category_.json" ]]; then
        cat > "$docs_dir/skills/_category_.json" << 'EOF'
{
  "label": "Skills Library",
  "position": 3,
  "link": {
    "type": "generated-index",
    "description": "Documentation for available skills."
  }
}
EOF
    fi

    log "INFO" "Docs directories ready"
}

# ---------------------------------------------------------------------------
# Set up versioning infrastructure
# ---------------------------------------------------------------------------
setup_versioning() {
    if [[ "$ENABLE_VERSIONING" != "true" ]]; then
        return 0
    fi

    local project_dir="${OUTPUT_DIR}/${PROJECT_NAME}"

    log "INFO" "Setting up versioning infrastructure..."

    # Create versions.json if it doesn't exist
    if [[ ! -f "$project_dir/versions.json" ]]; then
        echo '[]' > "$project_dir/versions.json"
    fi

    # Create versioned_docs and versioned_sidebars dirs
    mkdir -p "$project_dir/versioned_docs"
    mkdir -p "$project_dir/versioned_sidebars"

    log "INFO" "Versioning infrastructure ready"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    log "INFO" "=== Docusaurus initialization started ==="
    log "INFO" "Project: $PROJECT_NAME | Title: $SITE_TITLE | URL: $SITE_URL"

    validate_prerequisites
    scaffold_project
    install_plugins
    generate_config
    configure_custom_css
    configure_sidebars
    setup_docs_dirs
    setup_versioning

    log "INFO" "=== Docusaurus initialization complete ==="
    echo "[OK] Docusaurus initialized (project: ${PROJECT_NAME}, plugins: search-local, ideal-image, sitemap)"
}

main "$@"
