# Repository Analysis: claude-mem vs beads vs txtai

## Executive Summary

After analyzing **claude-mem** (8.7k stars) and **beads** (6.1k stars), neither is a drop-in replacement for txtai for codebase context retrieval. Here's the honest assessment:

---

## Repository 1: claude-mem

**URL**: https://github.com/thedotmack/claude-mem  
**Stars**: 8.7k  
**Language**: TypeScript  
**License**: AGPL-3.0

### What It Does

Captures **Claude Code IDE sessions** and stores them for later retrieval:
- Watches Claude Code interactions in real-time
- Stores observations in SQLite + ChromaDB
- AI compresses/summarizes sessions
- Injects relevant context back into future Claude Code sessions

### Architecture

```
Claude Code IDE → Plugin → SQLite DB + ChromaDB → AI Compression → Context Injection
```

**Storage**:
- SQLite for structured data (observations, sessions, prompts)
- ChromaDB for vector embeddings (semantic search)
- Files: `~/.claude-mem/claude-mem.db` + ChromaDB files

**Key Features**:
- Session timeline reconstruction
- Semantic search over coding history
- Context hooks for Claude Code
- MCP server for Claude integration
- Automatic compression/summarization

### Strengths

✅ **Battle-tested**: 8.7k stars, active development (hours ago)  
✅ **Purpose-built**: Specifically for Claude Code workflow  
✅ **AI compression**: Smart summarization to save tokens  
✅ **Real-time capture**: Watches as you code  
✅ **SQLite storage**: File-based, portable  

### Weaknesses for Your Use Case

❌ **Claude Code only**: Only works with Claude Code IDE  
❌ **Session-focused**: Captures interactions, not codebase analysis  
❌ **AGPL-3.0 license**: Infectious copyleft (must open-source derivatives)  
❌ **No AST parsing**: Doesn't understand code structure  
❌ **No BM25**: Only semantic search via ChromaDB  
❌ **No chunking**: Stores whole sessions, not file chunks  
❌ **Not for general agents**: Tied to Claude Code plugin system  

### Use Case Match: 3/10

**Good if**: You only use Claude Code IDE and want to remember past sessions  
**Bad for**: Self-hosted agents, software-agnostic solution, codebase indexing

---

## Repository 2: beads

**URL**: https://github.com/steveyegge/beads  
**Stars**: 6.1k  
**Language**: Go (92%)  
**License**: MIT

### What It Does

**Git-backed graph issue tracker for AI agents**:
- Creates task/issue database in `.beads/` directory
- Stores tasks as JSONL files (`issues.jsonl`)
- Git-versioned (committed to repo)
- Dependency tracking between tasks
- Auto-ready task detection

### Architecture

```
Agent → bd CLI → JSONL files (.beads/issues.jsonl) → Git repo
```

**Storage**:
- JSONL files in `.beads/` directory
- SQLite cache for performance (optional)
- Git repository for version control

**Key Features**:
- Task dependency graph
- Hash-based IDs (no merge conflicts)
- Auto-compaction ("memory decay")
- Multi-agent / multi-branch support
- Works with any AI agent (via AGENTS.md instructions)

### Strengths

✅ **Proven**: 6.1k stars, used by many  
✅ **File-based**: JSONL files, git-versioned  
✅ **Agent-agnostic**: Works with any AI agent  
✅ **Self-hosted**: No external services  
✅ **MIT license**: Commercial-friendly  
✅ **Horizontal scaling**: Multi-agent support  

### Weaknesses for Your Use Case

❌ **Task tracking only**: For issues/tasks, not codebase indexing  
❌ **No code parsing**: Doesn't analyze source files  
❌ **No search**: No BM25, semantic search, or embeddings  
❌ **No chunking**: Stores whole tasks, not file chunks  
❌ **No MCP**: No Model Context Protocol integration  
❌ **Different domain**: Project management ≠ code retrieval  

### Use Case Match: 2/10

**Good if**: You want AI agents to track tasks/issues in git  
**Bad for**: Codebase context retrieval, semantic search

---

## Comparison: txtai vs claude-mem vs beads

| Feature | txtai | claude-mem | beads |
|---------|-------|-----------|-------|
| **Primary Use** | Codebase indexing | Session memory | Task tracking |
| **Search** | BM25 + Semantic + RRF | Semantic only | None |
| **File-based** | ✓ Pure files | SQLite + ChromaDB | ✓ JSONL |
| **Code-aware** | ✓ AST chunking | ✗ No parsing | ✗ No parsing |
| **MCP Integration** | ✓ Built-in | ✓ For Claude | ✗ None |
| **Software-agnostic** | ✓ Any agent | ✗ Claude only | ✓ Any agent |
| **Self-hosted** | ✓ Pure Python | ✓ Node.js | ✓ Go binary |
| **License** | Apache 2.0 | AGPL-3.0 | MIT |
| **Stars** | 12k | 8.7k | 6.1k |
| **For Codebases** | ✓ Yes | ✗ No | ✗ No |

---

## Analysis

### Neither Repository Solves Your Problem

**Your requirements**:
- ✓ File-based storage
- ✓ Software-agnostic
- ✓ Self-hosted
- ✓ Hybrid search (BM25 + semantic)
- ✓ RRF fusion
- ✓ Code-aware chunking

**claude-mem provides**:
- ✓ File-based (SQLite)
- ✗ Software-agnostic (Claude Code only)
- ✓ Self-hosted
- ✗ BM25 (semantic only)
- ✗ RRF (not needed for sessions)
- ✗ Code-aware (no parsing)

**beads provides**:
- ✓ File-based (JSONL)
- ✓ Software-agnostic
- ✓ Self-hosted
- ✗ BM25 (not a search tool)
- ✗ RRF (not a search tool)
- ✗ Code-aware (not for code)

### What About Extracting Components?

#### From claude-mem:
- **Session capture**: Irrelevant (you're indexing code, not sessions)
- **ChromaDB integration**: You'd still need BM25 + RRF
- **AI compression**: Interesting but orthogonal to search
- **SQLite schema**: For observations, not code chunks

**Verdict**: Would need to rewrite 90% for codebase indexing

#### From beads:
- **JSONL storage**: Good pattern, but beads stores tasks, not code
- **Git versioning**: Nice, but txtai also supports this
- **Dependency graph**: For tasks, not code imports
- **Hash-based IDs**: Useful, but txtai already has IDs

**Verdict**: Wrong abstraction layer (project management)

---

## Conclusion

**Use txtai, not these repositories**.

### Why txtai is Still the Right Choice

1. **Purpose-built**: txtai is designed for semantic search over documents/code
2. **All-in-one**: BM25 + embeddings + RRF + file storage + MCP
3. **Code-aware**: Has CodeSplitter with tree-sitter
4. **Less work**: 15 min setup vs weeks extracting/rewriting
5. **Better fit**: Matches your requirements 100%

### When claude-mem/beads Might Be Useful

- **claude-mem**: If you use Claude Code IDE heavily and want session memory
- **beads**: If your agents need to track long-term tasks/issues in git
- **Both**: Could be used alongside txtai (different purposes)

### Recommendation

```
.txtai/                    # Codebase context index (for RAG)
├── embeddings/           # Vector search
├── keywords/             # BM25 search
└── manifest.json

.beads/                    # Agent task tracking (for project management)
└── issues.jsonl          # Task database

.claude-mem/              # Session memory (if using Claude Code)
└── claude-mem.db         # Session history
```

**Three different tools for three different jobs**:
- **txtai** = "What code exists and what does it do?"
- **beads** = "What tasks need to be done?"
- **claude-mem** = "What have we discussed before?"

---

## Deeper Dive: Architecture Mismatch

### claude-mem's Design Philosophy

**Captures**: Claude ←→ User interactions  
**Stores**: Sessions, observations, prompts  
**Searches**: Semantic similarity to past sessions  
**Goal**: "Remember what we did last time"

**Why it doesn't work for codebases**:
- No file parsing (just captures text output)
- No AST analysis (doesn't understand structure)
- Chunks at session boundaries (not semantic boundaries)
- Tied to Claude Code plugin API

### beads' Design Philosophy

**Captures**: Agent decisions about tasks  
**Stores**: Issues, dependencies, status  
**Searches**: ID lookups, dependency traversal  
**Goal**: "Track what needs to be done"

**Why it doesn't work for codebases**:
- Stores tasks, not code
- No parsing of source files
- No search across code content
- No understanding of code relationships

### txtai's Design Philosophy

**Captures**: Source code files  
**Stores**: Code chunks, embeddings, BM25 index  
**Searches**: Hybrid (BM25 + semantic + RRF)  
**Goal**: "Find relevant code for any query"

**Why it works for codebases**:
- AST-aware chunking
- Multiple search modalities
- File-based storage
- MCP integration
- Language-agnostic

---

## Final Verdict

**Don't use claude-mem or beads for codebase context retrieval**.

**Do use**:
- **txtai** for codebase indexing/search (what we discussed)
- **beads** (optional) for agent task tracking (separate concern)
- **claude-mem** (optional) if using Claude Code IDE (separate concern)

These are **complementary tools, not alternatives**.
