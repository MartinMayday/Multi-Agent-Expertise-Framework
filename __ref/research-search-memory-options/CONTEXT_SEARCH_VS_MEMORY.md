# Context-Search vs Context-Memory: Defining the Terms

## Core Question

**Which should you focus on?**
- Context-Search = Finding relevant code snippets on demand
- Context-Memory = Remembering and retrieving past agent information

### Your Use Case = Context-Search (Primary)

**What you're asking agents to do**:
```
Agent: "Find the payment retry logic in this codebase"
    ↓
SEARCH: Query against code/functions/symbols
    ↓
RETURN: lines 180-240 of payment_service.py
    ↓
USE: Provide as context for LLM to answer
```

**Key characteristics**:
- ✓ Codebase content is the source of truth
- ✓ Searching for specific logic, functions, patterns
- ✓ Retrieval based on semantic/code similarity
- ✓ One-time query → immediate answer
- ✓ Stateless per request

**Tools that implement this**:
- ✓ txtai (embeddings DB + search)
- ✓ ck-search (grep replacement)
- ✓ Both are Context-Search tools

---

### Context-Memory (Not Your Priority)

**What would be different**:
```
Agent: "What did we decide about error handling last Tuesday?"
    ↓
MEMORY: Search past agent sessions/decisions
    ↓
RETURN: "We decided to use exponential backoff for payment retries"
    ↓
USE: Apply that decision to current task
```

**Key characteristics**:
- ✗ Remembering past conversations
- ✗ Agent state management
- ✗ Decision tracking across sessions
- ✗ Historical knowledge base
- ✗ Stateful across requests

**Tools that implement this**:
- ✗ claude-mem (session memory)
- ✗ beads (task tracking)
- ✗ Different tools from codebase search

---

## Concrete Examples

### Scenario 1: "Find the retry logic"

**Context-Search** (You need this):
```python
# Input: Agent query
query = "payment retry backoff logic"

# Process: Search codebase index
results = embeddings.search(query, k=5)

# Output: Relevant code chunks
for result in results:
    print(f"{result['path']}:{result['line_start']}")
    print(result['text'][:300])
```

**This is what txtai/ck-search provide**

---

### Scenario 2: "What did we decide about retries?"

**Context-Memory** (You don't need this):
```python
# Input: Memory query
query = "decisions about retry logic from last week"

# Process: Search agent memory/session history
results = memory.search(query, date_range="last 7 days")

# Output: Past conversations/decisions
for result in results:
    print(f"Session {result['session_id']}")
    print(result['decision_summary'])
```

**This is what claude-mem provides** (not needed for your use case)

---

## Why This Matters

### The Architecture Difference

**Context-Search Architecture**:
```
┌─────────────────────────────────────┐
│       Agent Query Handler          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│         Embeddings Database         │  ← txtai/ck-search
│  (BM25 + semantic + hybrid search) │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Code Chunks from Source Files    │  ← Source of truth
└─────────────────────────────────────┘
```

**Key**: Codebase is the source of all knowledge. Index is rebuilt from source files.

**Context-Memory Architecture**:
```
┌─────────────────────────────────────┐
│      Agent Session Handler         │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│        Memory Database              │  ← claude-mem/beads
│  (Sessions, decisions, tasks)      │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Past Agent Conversations         │  ← Source of truth
└─────────────────────────────────────┘
```

**Key**: Agent history is the source of knowledge. Database accumulates over time.

---

## Your Focus Should Be: Context-Search

### Priority 1: Codebase Indexing (Context-Search)

**Goal**: Enable any AI agent to find relevant code instantly

**Requirements**:
- ✓ BM25 lexical search for exact matches
- ✓ Semantic embeddings for meaning-based search
- ✓ RRF fusion for optimal ranking
- ✓ AST-aware chunking for code understanding
- ✓ File-based storage (portable, versionable)
- ✓ MCP integration for agent access

**Tools**: txtai OR ck-search (both work)

**Implementation**:
```python
# With txtai
from txtai import Embeddings
embeddings = Embeddings(hybrid=True, content=True)
embeddings.index(document_stream())
embeddings.save(".ai-index/txtai")

# With ck (already installed!)
# cd /path/to/project && ck --index .
```

**Output**: Agents can search code by concept, not just keywords

---

### Priority 2: Agent Instructions (Context-Memory Lite)

**Goal**: Help agents know how to use the codebase

**Requirements**:
- ✓ Project conventions (.cursor/rules/, .context/)
- ✓ Architecture documentation
- ✓ LLM-friendly formats (llms.txt, .context/index.md)

**Tools**:
- Manual: `.context/index.md` files
- Auto-generated: llms.txt from txtai
- Framework: Codebase Context Specification

**Implementation**:
```bash
# With txtai
python scripts/index-repo.py  # Generates llms.txt

# Manual
mkdir -p .context
echo "# Project Context" > .context/index.md
```

**Output**: Agents understand project structure without being told each time

---

### Priority 3: Task Tracking (Optional Context-Memory)

**Goal**: Optional - track what agents are working on

**Requirements**:
- ✓ Issue/task database
- ✓ Dependency tracking
- ✓ Git-backed (versioned)

**Tools**: beads (optional)

**When to add**:
- Multiple agents working on same project
- Long-running tasks spanning sessions
- Need to track agent decisions

**Implementation**:
```bash
# If needed later
pip install beads-mcp
bd init
```

**Output**: Agents remember what they're supposed to be doing

---

## Decision Tree

```
Q: "What's my primary goal?"
    │
    ├─ "Enable agents to find code in my codebase" → Context-Search
    │   │
    │   ├─ "I'm building Python agents" → txtai
    │   ├─ "I use CLI interactively" → ck-search
    │   └─ "Both" → Use both! (they're complementary)
    │
    └─ "Enable agents to remember past work" → Context-Memory
        │
        ├─ "I use Claude Code IDE" → claude-mem
        ├─ "I need task tracking" → beads
        └─ "Both" → Use both!
```

**Your path**: Context-Search → txtai or ck-search

---

## My Recommendation: Use BOTH (They're complementary)

### 1. Start with ck-search (Today)

```bash
# Already installed!
cd /path/to/project
ck --index .                    # Build index
ck --hybrid "payment retry"     # Search code
```

**Use for**:
- Interactive development
- Quick searches
- Exploration via TUI

### 2. Add txtai (Tomorrow, for agents)

```python
# For Python agents
from txtai import Embeddings
embeddings = Embeddings()
embeddings.load(".ai-index/txtai")

# In agent
results = embeddings.search(query, 10)
```

**Use for**:
- Python-based agents
- MCP integration
- Complex RAG pipelines

### 3. Add beads (Next week, if needed)

```bash
# If you need task tracking
pip install beads-mcp
bd init
```

**Use for**:
- Task management
- Multi-agent coordination
- Long-running projects

---

## Summary: What to Focus On

### Focus Area 1: Context-Search (CRITICAL)
**Tool**: txtai OR ck-search  
**Time**: 15 minutes to start  
**Value**: Enables all agents to find code

### Focus Area 2: Project Context (HIGH)
**Tool**: llms.txt + .context/index.md  
**Time**: 30 minutes to write  
**Value**: Agents understand your project

### Focus Area 3: Task Memory (OPTIONAL)
**Tool**: beads (if needed)  
**Time**: Add when you hit limits  
**Value**: Track agent work over time

---

## Final Answer

**Q: "Context-search or context-memory?"**

**A: Context-search is your PRIMARY focus. Context-memory is secondary/optional.**

**Q: "txtai or ck-search?"**

**A: Use ck-search for interactive CLI work (you already have it!). Use txtai for Python agents and MCP integration.**

They're both file-based, both do hybrid search, both are production-ready. They solve the same problem but for different interfaces (CLI vs Python API).

**You can't go wrong with either - they both solve your core need.**
