---
name: agents-md-gen
description: Generate AGENTS.md documentation for any project to teach AI agents about the codebase
version: 1.0.0
allowed-tools:
  - Bash(python*)
  - Read
  - Write
---

# agents-md-gen

Generate comprehensive AGENTS.md files that teach AI agents about any codebase.

## When to Use

Use this skill when:
- Setting up a new project for AI-assisted development
- Onboarding AI agents to an existing codebase
- Updating project documentation after major changes
- Creating standardized AI guidance for monorepos

## Instructions

### Basic Usage

```bash
# Generate AGENTS.md for current directory
python skills/agents-md-gen/scripts/generate_agents_md.py .

# Generate for specific project
python skills/agents-md-gen/scripts/generate_agents_md.py /path/to/project

# Dry run (preview without writing)
python skills/agents-md-gen/scripts/generate_agents_md.py . --dry-run

# Verbose output
python skills/agents-md-gen/scripts/generate_agents_md.py . --verbose

# Cleanup generated file
python skills/agents-md-gen/scripts/generate_agents_md.py . --cleanup
```

### Validation

```bash
# Validate generated AGENTS.md
python skills/agents-md-gen/scripts/validate_agents_md.py /path/to/AGENTS.md
```

### Debug Mode

```bash
# Enable debug logging
DEBUG=1 python skills/agents-md-gen/scripts/generate_agents_md.py .
```

## Validation Checklist

Before considering generation complete:
- [ ] AGENTS.md file exists at project root
- [ ] File size > 200 bytes (not empty)
- [ ] Contains `# AGENTS.md` header
- [ ] Contains `## Directory Structure` section
- [ ] Contains `## Technology Stack` section
- [ ] Contains `## Conventions` section
- [ ] Markdown syntax is valid
- [ ] At least 4 sections present

## Success Criteria

Output on success:
```
[OK] AGENTS.md generated (X bytes)
```

Output on validation:
```
[OK] AGENTS.md valid (4 sections, X bytes)
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Fatal error (IO, timeout) |
| 2 | Validation error (bad input) |

## Token Efficiency

This skill follows the MCP token efficiency pattern:
- SKILL.md: ~100 tokens (loads once)
- Scripts execute externally, not loaded into context
- Final output: ~10 tokens
- Total context impact: ~110 tokens
