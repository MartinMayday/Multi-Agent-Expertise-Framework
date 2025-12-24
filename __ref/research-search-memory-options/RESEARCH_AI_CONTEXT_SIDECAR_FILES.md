# Research: AI Context Sidecar Files & Progressive Context Loading

## Executive Summary

This research documents existing frameworks, protocols, and tools for generating sidecar/context files that enable AI/LLMs to retrieve relevant context from codebases. The goal is progressive context loading where AI pulls only content matching task/request with sufficient relevancy or maturity scores.

---

## Part 1: Established Protocols & Specifications

### 1.1 llms.txt Protocol

**Source**: https://llmstxt.org/  
**Author**: Jeremy Howard (Answer.AI, fast.ai)  
**Status**: Active, widely adopted

**Purpose**: Standardized file placed at `/llms.txt` providing LLM-friendly content about a website/project.

**Format Specification**:
```markdown
# Title

> Optional description goes here

Optional details go here

## Section name

- [Link title](https://link_url): Optional link details

## Optional

- [Link title](https://link_url)
```

**Key Features**:
- H1: Project name (required)
- Blockquote: Brief summary
- Sections: H2-delimited with file lists as markdown links
- "Optional" section: URLs that can be skipped for shorter context
- Companion files: `llms-full.txt` (all content), `llms-ctx.txt` (expanded context)

**Tooling**:
- `llms_txt2ctx` CLI for parsing/expanding
- VitePress plugin: `vitepress-plugin-llms`
- Docusaurus plugin: `docusaurus-plugin-llms`
- Drupal: LLM Support module

**Real-World Adoption**:
- FastHTML project
- Google A2A Protocol (Agents to Agents)
- nbdev projects (automatic .md versions)
- Multiple documentation platforms (Mintlify, etc.)

---

### 1.2 Codebase Context Specification (CCS)

**Source**: https://github.com/Agentic-Insights/codebase-context-spec  
**Status**: Archived (Oct 2025), v1.1.0-RFC  
**License**: MIT

**Structure**:
```
project-root/
├── .context/
│   ├── index.md          # Main context file (required)
│   ├── .context.yaml     # Optional structured metadata
│   └── .context.json     # Optional JSON metadata
├── .contextignore        # Files to exclude from context
└── CODEBASE-CONTEXT.md   # Full specification
```

**Key Concepts**:
- `.context` directory with `index.md` at project root
- Optional YAML/JSON for structured metadata
- `.contextignore` for exclusion patterns
- Hierarchical context at directory level
- CODING-ASSISTANT-PROMPT.md for AI instruction

**NPM Package**: `@codebase-context/cc-cli` (dotcontext)

---

### 1.3 Cursor Rules System

**Source**: https://cursor.com/docs/context/rules

**Structure**:
```
.cursor/rules/
└── my-rule/
    ├── RULE.md           # Main rule file with frontmatter
    └── scripts/          # Helper scripts (optional)
```

**Features**:
- Path-pattern scoping (globs)
- Manual or relevance-based invocation
- Domain-specific knowledge encoding
- Workflow automation templates
- Style/architecture standardization

---

## Part 2: Production Tools for Context Generation

### 2.1 Full Repository Packing Tools

| Tool | Stars | Language | Key Feature |
|------|-------|----------|-------------|
| [repomix](https://github.com/yamadashy/repomix) | 20,168 | TypeScript | Single AI-friendly file, MCP support, Claude Skills |
| [code2prompt](https://github.com/mufeedvh/code2prompt) | 6,740 | Rust | Prompt templating, token counting |
| [yek](https://github.com/bodo-run/yek) | 2,363 | Rust | Fast serialization for LLM consumption |
| [files-to-prompt](https://github.com/simonw/files-to-prompt) | 2,500 | Python | Directory concatenation |
| [gitingest](https://gitingest.com/) | - | Web | URL-based repo to text |

### 2.2 Intelligent Context Selection Tools

| Tool | Stars | Language | Key Feature |
|------|-------|----------|-------------|
| [llm-context.py](https://github.com/cyberchitta/llm-context.py) | 283 | Python | Rule-based selection, MCP, smart outlining |
| [repogather](https://github.com/gr-b/repogather) | 230 | Python | Relevance-based file selection |
| [codebase-digest](https://github.com/kamilstanuch/codebase-digest) | 316 | Python | 60+ prompts, structured metrics |

### 2.3 Documentation Generation Tools

| Tool | Stars | Purpose |
|------|-------|---------|
| [RepoAgent](https://github.com/OpenBMB/RepoAgent) | 862 | LLM-powered repo documentation |
| [DocuWriter.ai](https://docuwriter.ai) | - | MCP-ready documentation |
| [Mintlify](https://mintlify.com) | - | Auto llms.txt generation |

---

## Part 3: Aider's Repository Map Approach

**Source**: https://aider.chat/docs/repomap.html

**Mechanism**:
1. Uses **tree-sitter** for AST parsing
2. Creates concise map of classes, functions, signatures
3. Graph ranking algorithm for relevance scoring
4. Dynamic token budget optimization (default: 1k tokens)

**Map Format Example**:
```
aider/coders/base_coder.py:
⋮...
│class Coder:
│    abs_fnames = None
⋮...
│    @classmethod
│    def create(
│        self,
│        main_model,
│        edit_format,
│        io,
⋮...

aider/commands.py:
⋮...
│class Commands:
│    voice = None
⋮...
```

**Benefits**:
- Shows classes, methods, function signatures
- Includes critical definition lines
- Uses dependency graph for ranking
- Adapts to chat context state

---

## Part 4: Recommended Implementation Approaches

### Approach A: llms.txt + Per-Folder Index (Lightweight)

**Best for**: Documentation sites, API references, smaller codebases

**Implementation**:
1. Generate root `/llms.txt` with project overview
2. Create `/llms-full.txt` with expanded content
3. Generate `.md` versions of key pages
4. Create per-folder `README.llm.md` summaries

**Script Example**:
```bash
#!/bin/bash
# generate-llms-txt.sh

echo "# $(basename $PWD)" > llms.txt
echo "" >> llms.txt
echo "> $(head -1 README.md | sed 's/^# //')" >> llms.txt
echo "" >> llms.txt

echo "## Core Files" >> llms.txt
for file in $(find . -name "*.py" -o -name "*.ts" | head -20); do
  echo "- [$file]($file): $(head -5 $file | grep -E '^#|^\"\"\"' | head -1)" >> llms.txt
done
```

---

### Approach B: .context Directory (Hierarchical)

**Best for**: Large monorepos, multi-module projects

**Implementation**:
```
project/
├── .context/
│   └── index.md           # Project-level context
├── src/
│   ├── .context/
│   │   └── index.md       # src-level context
│   └── api/
│       ├── .context/
│       │   └── index.md   # API module context
│       └── handlers.py
```

**index.md Template**:
```markdown
# Module: API

## Purpose
Handles HTTP request routing and response formatting.

## Key Components
- `handlers.py`: Request handlers for REST endpoints
- `middleware.py`: Authentication and logging middleware

## Dependencies
- `../models/` - Data models
- `../services/` - Business logic

## Conventions
- All handlers return ResponseModel
- Authentication via Bearer tokens
```

---

### Approach C: Sidecar Files with AST Analysis (Advanced)

**Best for**: Code-heavy projects needing relevance scoring

**Implementation**:
1. Parse each file with tree-sitter
2. Extract symbols, dependencies, call graphs
3. Generate `.context.md` sidecar per file
4. Score relevance based on:
   - Reference count (how often used)
   - Dependency depth
   - API surface visibility (exported vs internal)

**Sidecar Format**:
```markdown
<!-- filepath.context.md -->
# Context: handlers.py

## Summary
HTTP request handlers for user management API.

## Symbols
| Name | Type | Visibility | References |
|------|------|------------|------------|
| create_user | function | public | 12 |
| UserHandler | class | public | 8 |
| _validate | function | private | 3 |

## Dependencies (imports)
- models.User
- services.UserService
- utils.validators

## Dependents (imported by)
- routes.py
- tests/test_handlers.py

## Relevance Score: 0.85
High-traffic entry point for user operations.
```

---

### Approach D: Unified Folder Index (AI-Powered)

**Best for**: Progressive loading with relevance scoring

**Implementation**:
```
project/
├── .ai-index/
│   ├── manifest.json      # File metadata + scores
│   ├── symbols.json       # Extracted symbols
│   └── dependencies.json  # Dependency graph
├── src/
│   └── module/
│       ├── index.ts
│       └── .ai-summary.md # LLM-generated summary
```

**manifest.json Schema**:
```json
{
  "version": "1.0",
  "generated": "2025-12-22T00:00:00Z",
  "files": [
    {
      "path": "src/api/handlers.py",
      "hash": "abc123",
      "lines": 150,
      "tokens": 1200,
      "relevance_score": 0.85,
      "maturity_score": 0.9,
      "categories": ["api", "user-management"],
      "symbols": ["create_user", "UserHandler"],
      "dependencies": ["models.User", "services.UserService"]
    }
  ]
}
```

---

## Part 5: Executable Workflow

### Option 1: Use Existing Tools

**For quick setup**:
```bash
# Install repomix
npm install -g repomix

# Generate context file
repomix --output context.txt

# Or use MCP server mode
repomix --mcp
```

**For rule-based selection**:
```bash
# Install llm-context
pip install llm-context

# Initialize
lc-init

# Select and generate
lc-select
lc-context -f output.md
```

### Option 2: RepoAgent for Documentation

```bash
# Install
pip install repoagent

# Configure (see .env requirements)
# Run documentation generation
repoagent
```

### Option 3: Custom Script (Python + tree-sitter)

See `generate-context-sidecars.py` in companion file.

---

## Part 6: Scoring & Relevance Metrics

### Relevance Score Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Reference Count | 0.25 | How often symbol is imported/called |
| API Surface | 0.20 | Public exports vs internal |
| File Size | 0.15 | Smaller = more focused |
| Recent Changes | 0.15 | Git activity recency |
| Documentation | 0.15 | Has docstrings/comments |
| Test Coverage | 0.10 | Associated test files |

### Maturity Score Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Age | 0.20 | Older = more stable |
| Commit Frequency | 0.20 | Low churn = mature |
| Code Complexity | 0.20 | Lower cyclomatic = mature |
| Error Rate | 0.20 | From logs/issues |
| Documentation | 0.20 | Well-documented = mature |

---

## Part 7: Recommendations

### For Your Use Case (Sidecar Files per File + Folder Index)

**Recommended Stack**:
1. **llms.txt** at root for project overview
2. **repomix** or **code2prompt** for full context generation
3. **tree-sitter** based custom script for sidecar generation
4. **.context/** directories for hierarchical context

**Priority Implementation**:
1. Start with llms.txt (5 minutes)
2. Add repomix to workflow (10 minutes)
3. Create .context/index.md files manually for key modules
4. Automate sidecar generation with custom script

---

## References

1. llms.txt Specification: https://llmstxt.org/
2. Codebase Context Spec: https://github.com/Agentic-Insights/codebase-context-spec
3. Aider Repository Map: https://aider.chat/docs/repomap.html
4. RepoAgent: https://github.com/OpenBMB/RepoAgent
5. Repomix: https://repomix.com/
6. 36 LLM Context Alternatives: https://www.cyberchitta.cc/articles/lc-alternatives.html
7. Cursor Rules: https://cursor.com/docs/context/rules
8. Tree-sitter: https://tree-sitter.github.io/
