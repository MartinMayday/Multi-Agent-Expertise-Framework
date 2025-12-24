# Quick Start: AI Context Sidecar Generation

## Option 1: Use Existing Tools (Fastest)

### A) Repomix (Most Popular - 20k+ stars)

```bash
# Install
npm install -g repomix

# Generate single context file
repomix

# With custom output
repomix --output llm-context.txt --style markdown

# As MCP server for Claude/Cursor
repomix --mcp
```

**Output**: Single file with entire codebase, token-counted, AI-optimized.

---

### B) llm-context.py (Rule-Based Selection)

```bash
# Install
pip install llm-context

# Initialize project
cd /your/project
lc-init

# Select files based on rules
lc-select

# Generate context (copies to clipboard)
lc-context

# Generate to file
lc-context -f context.md

# Switch between rule sets
lc-set-rule flt-base  # Different file filters
```

**Output**: Customizable context with rule-based file selection.

---

### C) code2prompt (Rust - Fast)

```bash
# Install
cargo install code2prompt

# Generate with template
code2prompt /path/to/project --template default
```

---

## Option 2: Custom Script (This Repo)

```bash
# Install dependencies
pip install gitpython

# Run the generator
python tmp/generate-context-sidecars.py /path/to/project

# Modes:
python tmp/generate-context-sidecars.py /path/to/project --mode sidecar      # Per-file .context.md
python tmp/generate-context-sidecars.py /path/to/project --mode folder-index # Folder summaries
python tmp/generate-context-sidecars.py /path/to/project --mode both         # Both (default)
python tmp/generate-context-sidecars.py /path/to/project --mode llms-txt     # llms.txt only
python tmp/generate-context-sidecars.py /path/to/project --mode manifest     # JSON manifest only

# Dry run (preview)
python tmp/generate-context-sidecars.py /path/to/project --dry-run
```

**Output Structure**:
```
project/
└── .ai-context/
    ├── llms.txt                    # Project overview
    ├── manifest.json               # Programmatic metadata
    ├── sidecars/
    │   ├── src_api_handlers.py.context.md
    │   └── src_models_user.py.context.md
    └── indexes/
        ├── root.index.md
        ├── src.index.md
        └── src_api.index.md
```

---

## Option 3: Manual llms.txt (Simplest)

Create `/llms.txt` in project root:

```markdown
# My Project

> Brief description of what this project does.

Important notes:
- Key architecture decisions
- Technologies used
- Conventions to follow

## Core

- [src/main.py](src/main.py): Application entry point
- [src/api/routes.py](src/api/routes.py): HTTP routing
- [src/models/](src/models/): Data models

## Optional

- [tests/](tests/): Test files
- [docs/](docs/): Documentation
```

---

## Comparison Table

| Approach | Setup Time | Automation | Relevance Scoring | Best For |
|----------|------------|------------|-------------------|----------|
| Repomix | 1 min | Full | No | Quick full-context |
| llm-context.py | 5 min | Rule-based | No | Task-specific contexts |
| Custom script | 10 min | Full | Yes | Progressive loading |
| Manual llms.txt | 5 min | None | Manual | Small projects |
| .context dirs | 15 min | None | Manual | Hierarchical docs |

---

## Recommended Workflow

1. **Start**: Create manual `llms.txt` (5 min)
2. **Scale**: Use `repomix` for full context when needed
3. **Optimize**: Run custom script for sidecar files + scoring
4. **Maintain**: Use pre-commit hooks to regenerate on changes

---

## Pre-commit Hook Example

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: ai-context-update
        name: Update AI Context Files
        entry: python scripts/generate-context-sidecars.py . --mode llms-txt
        language: system
        pass_filenames: false
        types: [python]
```

---

## MCP Integration

For Claude Desktop or Cursor with MCP:

```json
{
  "mcpServers": {
    "repomix": {
      "command": "npx",
      "args": ["repomix", "--mcp"]
    }
  }
}
```

Or with llm-context.py MCP server.
