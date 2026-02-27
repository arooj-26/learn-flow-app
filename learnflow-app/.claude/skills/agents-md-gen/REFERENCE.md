# agents-md-gen Reference

Complete reference documentation for the AGENTS.md generator skill.

## Configuration Options

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `path` | Project path to analyze | Required |
| `--dry-run` | Preview without writing | False |
| `--verbose` | Detailed output | False |
| `--cleanup` | Remove generated AGENTS.md | False |
| `--max-depth` | Directory scan depth | 4 |
| `--output` | Custom output filename | AGENTS.md |

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug logging | 0 |
| `AGENTS_LOG_FILE` | Log file path | .agents-gen.log |
| `AGENTS_TIMEOUT` | Operation timeout (seconds) | 30 |

## Supported Project Types

### Node.js Projects

Detection: `package.json` present

Generated sections:
- Package name and version
- Dependencies overview
- Scripts available
- Entry points

Example output:
```markdown
## Technology Stack
- **Runtime**: Node.js
- **Package Manager**: npm/yarn/pnpm
- **Framework**: Express/Next.js/etc.
- **Dependencies**: X production, Y development
```

### Python Projects

Detection: `pyproject.toml`, `setup.py`, or `requirements.txt` present

Generated sections:
- Python version requirements
- Dependencies overview
- Entry points/main modules
- Virtual environment info

Example output:
```markdown
## Technology Stack
- **Runtime**: Python 3.x
- **Package Manager**: pip/poetry/uv
- **Framework**: Django/Flask/FastAPI/etc.
- **Dependencies**: X packages
```

### Monorepo Projects

Detection: `pnpm-workspace.yaml`, `lerna.json`, or `packages/` directory

Generated sections:
- Workspace structure
- Shared dependencies
- Package relationships
- Build order recommendations

Example output:
```markdown
## Directory Structure
- **packages/**: Workspace packages
  - `core/`: Shared utilities
  - `web/`: Frontend application
  - `api/`: Backend services
```

### Unknown Projects

When no specific type detected:
- Basic directory analysis
- File type statistics
- Common patterns detected
- Generic conventions

## Customization

### Adding Custom Sections

Create `.agents-config.json` in project root:

```json
{
  "customSections": [
    {
      "title": "Deployment",
      "content": "Deploy via GitHub Actions to AWS ECS."
    }
  ],
  "excludeDirs": ["node_modules", ".git", "dist"],
  "maxDepth": 3
}
```

### Template Override

Create `.agents-template.md` in project root for custom template:

```markdown
# AGENTS.md

{{PROJECT_NAME}}

## Overview
{{DESCRIPTION}}

## Custom Section
Your static content here.

## Directory Structure
{{DIRECTORY_STRUCTURE}}

## Technology Stack
{{TECH_STACK}}

## Conventions
{{CONVENTIONS}}
```

## Troubleshooting

### Problem: "Path does not exist"

**Cause**: Invalid project path provided.

**Solution**:
```bash
# Verify path exists
ls -la /path/to/project

# Use absolute path
python scripts/generate_agents_md.py "$(pwd)"
```

### Problem: "Permission denied"

**Cause**: Cannot read project directory or write AGENTS.md.

**Solution**:
```bash
# Check permissions
ls -la /path/to/project

# Fix permissions
chmod +r /path/to/project

# Run with sudo if needed (not recommended)
sudo python scripts/generate_agents_md.py /path/to/project
```

### Problem: "Analysis timeout (>30s)"

**Cause**: Project too large or slow filesystem.

**Solution**:
```bash
# Increase timeout
AGENTS_TIMEOUT=60 python scripts/generate_agents_md.py .

# Reduce scan depth
python scripts/generate_agents_md.py . --max-depth 2

# Exclude large directories in .agents-config.json
```

### Problem: "AGENTS.md validation failed"

**Cause**: Generated file missing required sections.

**Solution**:
```bash
# Check what sections are present
python scripts/validate_agents_md.py AGENTS.md --verbose

# Regenerate with verbose mode
python scripts/generate_agents_md.py . --verbose

# Check debug log
cat .agents-gen.log
```

### Problem: "Empty AGENTS.md generated"

**Cause**: No analyzable content found in project.

**Solution**:
```bash
# Verify project has content
find . -type f -name "*.py" -o -name "*.js" -o -name "*.ts" | head

# Check for hidden files only
ls -la

# Run in verbose mode to see what's detected
python scripts/generate_agents_md.py . --verbose
```

## Examples

### Node.js Project

```bash
cd my-express-app
python /path/to/skills/agents-md-gen/scripts/generate_agents_md.py .
```

Output AGENTS.md:
```markdown
# AGENTS.md

Documentation for AI agents working with my-express-app.

## Directory Structure

```
my-express-app/
├── src/
│   ├── routes/      # API route handlers
│   ├── middleware/  # Express middleware
│   ├── models/      # Data models
│   └── index.js     # Entry point
├── tests/           # Test files
├── package.json     # Dependencies
└── .env.example     # Environment template
```

## Technology Stack

- **Runtime**: Node.js 18.x
- **Framework**: Express 4.x
- **Database**: PostgreSQL (via pg)
- **Testing**: Jest
- **Linting**: ESLint + Prettier

## Conventions

- Use async/await for asynchronous operations
- Follow REST conventions for API routes
- Place business logic in services/, not routes/
- Use environment variables for configuration
```

### Python Project

```bash
cd my-fastapi-app
python /path/to/skills/agents-md-gen/scripts/generate_agents_md.py .
```

Output AGENTS.md:
```markdown
# AGENTS.md

Documentation for AI agents working with my-fastapi-app.

## Directory Structure

```
my-fastapi-app/
├── app/
│   ├── api/         # API endpoints
│   ├── core/        # Configuration
│   ├── models/      # Pydantic models
│   └── main.py      # FastAPI app
├── tests/           # Pytest tests
├── pyproject.toml   # Dependencies
└── .env.example     # Environment template
```

## Technology Stack

- **Runtime**: Python 3.11
- **Framework**: FastAPI 0.100+
- **Database**: SQLAlchemy + PostgreSQL
- **Testing**: pytest
- **Linting**: ruff

## Conventions

- Use type hints for all function signatures
- Follow PEP 8 style guidelines
- Place schemas in models/, not api/
- Use dependency injection for services
```

### Monorepo Project

```bash
cd my-monorepo
python /path/to/skills/agents-md-gen/scripts/generate_agents_md.py .
```

Output AGENTS.md:
```markdown
# AGENTS.md

Documentation for AI agents working with my-monorepo.

## Directory Structure

```
my-monorepo/
├── packages/
│   ├── core/        # Shared utilities (@myorg/core)
│   ├── ui/          # Component library (@myorg/ui)
│   ├── web/         # Next.js frontend
│   └── api/         # Express backend
├── tools/           # Build scripts
├── pnpm-workspace.yaml
└── turbo.json       # Turborepo config
```

## Technology Stack

- **Monorepo**: pnpm workspaces + Turborepo
- **Frontend**: Next.js 14, React 18
- **Backend**: Express, tRPC
- **Shared**: TypeScript 5.x
- **Testing**: Vitest

## Conventions

- Import shared packages via @myorg/* aliases
- Run commands from root: `pnpm --filter @myorg/web dev`
- Changes to core/ require rebuilding dependents
- Use changesets for versioning
```

## Log Format

Debug logs follow this pattern:
```
[2024-01-15T10:30:45.123Z] [INFO] Starting analysis of /path/to/project
[2024-01-15T10:30:45.456Z] [DEBUG] Detected project type: nodejs
[2024-01-15T10:30:46.789Z] [DEBUG] Found 15 directories, 42 files
[2024-01-15T10:30:47.012Z] [INFO] Generated AGENTS.md (1234 bytes)
```

## API Reference

### generate_agents_md.py

```python
def analyze_project(path: str, max_depth: int = 4) -> ProjectInfo
def detect_project_type(path: str) -> str  # nodejs|python|monorepo|unknown
def generate_directory_structure(path: str, max_depth: int) -> str
def generate_tech_stack(project_info: ProjectInfo) -> str
def generate_conventions(project_info: ProjectInfo) -> str
def write_agents_md(path: str, content: str, dry_run: bool = False) -> int
```

### validate_agents_md.py

```python
def validate_file_exists(path: str) -> bool
def validate_file_size(path: str, min_bytes: int = 200) -> bool
def validate_markdown_syntax(content: str) -> bool
def validate_required_sections(content: str) -> tuple[bool, list[str]]
def validate_agents_md(path: str) -> tuple[bool, str]
```
