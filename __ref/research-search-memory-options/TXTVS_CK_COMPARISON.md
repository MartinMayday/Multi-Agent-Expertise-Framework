# txtai vs ck-search Comparison

## Executive Summary

**You already have ck-search (ck) installed!** It's a Rust-based tool that provides hybrid search (BM25 + semantic) very similar to txtai, but with a different focus.

**Key differences**:
- **ck-search**: CLI tool, faster for interactive use, Rust-based, local-first, simpler
- **txtai**: Python library, more features (MCP, workflows, pipelines), extendable

**For your use case**: Both work! ck is simpler for CLI/interactive use; txtai is better for Python integration and self-hosted agents.

---

## Side-by-Side Comparison

### Basic Info

| Feature | txtai | ck-search |
|---------|-------|-----------|
| **Language** | Python | Rust |
| **Stars** | 12k | 1.1k |
| **License** | Apache 2.0 | Apache 2.0 / MIT |
| **Primary Use** | Embeddings DB / RAG | CLI code search |
| **Installation** | `pip install txtai` | `cargo install ck-search` |
| **You have it?** | Need to install | ✅ Already installed! |

### Architecture

```
txtai:
--------
Python lib → Embeddings database → File storage → MCP → Agents

ck-search:
----------
Rust CLI → Index + embeddings → .ck/ directory → stdout → Humans/Scripts
```

### Feature Comparison

#### ✅ Both Provide

| Feature | txtai | ck-search | Notes |
|---------|-------|-----------|-------|
| **BM25 lexical search** | ✓ Yes | ✓ Yes | Both use modern BM25 |
| **Semantic embeddings** | ✓ Yes | ✓ Yes | Both use FastEmbed |
| **Hybrid search** | ✓ Yes | ✓ Yes | Both combine BM25 + semantic |
| **RRF fusion** | ✓ Yes (built-in) | ✓ Yes (`--hybrid`) | Both use reciprocal rank |
| **Tree-sitter chunking** | ✓ Yes | ✓ Yes | Both AST-aware |
| **File-based storage** | ✓ Yes | ✓ Yes | Both pure files |
| **Multiple languages** | ✓ 10+ langs | ✓ 7+ langs | Similar coverage |
| **Incremental indexing** | ✓ Yes | ✓ Yes | Both smart about changes |
| **Offline operation** | ✓ Yes | ✓ Yes | Both local-first |

#### ❌ Differences

| Feature | txtai | ck-search | Winner |
|---------|-------|-----------|--------|
| **Python API** | ✓ Full library | ✗ CLI only | txtai |
| **MCP server** | ✓ Built-in | ✓ Built-in | Tie |
| **Workflows** | ✓ Yes | ✗ No | txtai |
| **Pipelines** | ✓ Yes (LLM, QA, etc) | ✗ No | txtai |
| **Graph networks** | ✓ Yes | ✗ No | txtai |
| **Multimodal** | ✓ Images, audio, video | ✗ Text only | txtai |
| **CLI speed** | ~Slower (Python) | ~Faster (Rust) | ck |
| **Interactive TUI** | ✗ No | ✓ Yes (`--tui`) | ck |
| **Memory usage** | ~Higher | ~Lower (Rust) | ck |
| **JSON output** | ✓ Yes | ✓ Yes (`--json`) | Tie |
| **JSONL output** | ✓ Yes | ✓ Yes (`--jsonl`) | Tie |
| **VS Code ext** | ✗ No | ✓ Yes | ck |
| **Config files** | ✗ Manual | ✓ `.ckignore` | ck |
| **Quick start** | `pip install txtai` | Already installed! | ck |

---

## Search Quality Comparison

Both tools should give similar results for code search since they use:
- Same BM25 algorithm
- Same embedding models (FastEmbed)
- Similar RRF fusion
- Similar chunking strategies

**Where they differ**:
- **txtai**: More knobs to tune, better for complex RAG pipelines
- **ck**: Optimized for interactive use, faster startup

---

## Use Case Scenarios

### Scenario 1: Interactive CLI Search

**Use ck-search**

```bash
# Index and search in one command
cd /path/to/project
ck --hybrid "payment retry logic"

# Or use the TUI for exploration
ck --tui
```

**Why ck wins**:
- Faster startup (Rust compiled)
- Better CLI UX
- TUI for exploration
- Syntax highlighting
- Already installed!

### Scenario 2: Self-Hosted Python Agents

**Use txtai**

```python
from txtai import Embeddings

embeddings = Embeddings()
embeddings.load(".ai-index/txtai")

# In your agent
results = embeddings.search("payment retry", 10)
context = build_context_from_results(results)
llm_call(context, query)
```

**Why txtai wins**:
- Python API for easy integration
- MCP server built-in
- More flexible for RAG pipelines
- Can embed in agent process

### Scenario 3: MCP Integration

**Both work!**

**ck MCP**:
```json
{
  "mcpServers": {
    "ck": {
      "command": "ck",
      "args": ["--mcp-daemon"],
      "env": {"CK_DIR": "/path/to/project"}
    }
  }
}
```

**txtai MCP**:
```python
# Python script
from txtai.mcp import MCPServer
server = MCPServer(embeddings)
server.run()
```

**Comparison**:
- ck: More mature MCP implementation (daemon mode)
- txtai: Easier to customize, Python integration

---

## Performance Comparison

### Based on tool design

| Metric | txtai (Python) | ck-search (Rust) |
|--------|---------------|------------------|
| **Startup time** | ~0.5-1s | ~0.05-0.1s |
| **Search latency** | ~10-50ms | ~5-20ms |
| **Memory usage** | ~100MB+ | ~20-50MB |
| **Index build** | ~slower | ~faster |
| **Index size** | Similar | Similar |

**Note**: Rust is faster but both are "fast enough" for most use cases. Difference matters for:
- Very large codebases (100k+ files)
- Frequent CLI usage
- Resource-constrained environments

---

## Storage Format Comparison

### txtai storage:
```
.ai-index/txtai/
├── config              # Configuration
├── embeddings          # Dense vectors (mmap)
├── index               # Main index
├── keywords            # BM25 sparse index
├── documents           # Content
└── objects             # Optional binary objects
```

### ck-search storage:
```
project/.ck/
├── embeddings.json     # Dense vectors
├── ann_index.bin       # Approximate NN index
└── tantivy_index/      # BM25 index (Tantivy)
```

**Both**:
- Pure file-based
- Portable
- Rebuildable
- Git-ignorable

---

## Semantic Chunking Comparison

### Both use tree-sitter:

```
txtai:
- ck-chunk crate (Rust backend)
- Python wrapper
- Supports 10+ languages

ck-search:
- Built-in ck-chunk crate
- Native Rust
- Supports 7+ languages
```

**Quality**: Similar, both use same underlying tree-sitter parsers

---

## When to Use Which

### Use ck-search (Rust) when:

✅ You need **interactive CLI search**
✅ You want **fast startup** 
✅ You prefer **TUI for exploration**
✅ You use **VS Code** (has extension)
✅ You care about **memory efficiency**
✅ You want **zero Python dependency**
✅ You need **configuration files** (.ckignore)

### Use txtai (Python) when:

✅ You're building **Python agents**
✅ You need **MCP integration**
✅ You want **workflows & pipelines**
✅ You need **multimodal search** (images, audio)
✅ You want **graph networks**
✅ You prefer **Python API over CLI**
✅ You need **custom processing logic**

---

## The **Answer to Your Second Question**

### "Context-Search" vs "Context-Memory" - Which to Focus?

**Context-Search** = Finding relevant code snippets on demand
**Context-Memory** = Remembering and retrieving past information

#### Your Requirements = Context-Search (Primary)

```
Agent: "Find the payment retry logic"
    ↓
SEARCH: Query codebase index
    ↓
RETURN: Relevant code chunks
    ↓
USE: As context for LLM generation
```

**This is pure search** - you're finding code, not remembering conversations or tasks.

#### Context-Memory (Secondary)

Would be:
```
Agent: "What did we decide about retries last week?"
    ↓
MEMORY: Search past decisions/agents
    ↓
RETURN: Previous conversation/task context
    ↓
USE: For continuity
```

**You don't need this** based on your requirements (self-hosted agents focusing on codebase content).

---

## Recommendation: Use Both (tl;dr)

### Phase 1: Start with ck-search (Today)

```bash
# Already installed!
cd /path/to/project
ck --index .                    # Build index
ck --hybrid