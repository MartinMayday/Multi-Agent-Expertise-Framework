# Full Coverage Architecture: Ensuring 100% Content Discoverability

## The Core Problem

```
┌─────────────────────────────────────────────────────────────┐
│  5MB gitingest file or large codebase                       │
│  ════════════════════════════════════════════════════════   │
│  [First 2000 chars] [Rest of content... INVISIBLE TO LLM]   │
│        ↑                        ↑                           │
│     AI sees this            AI never sees this              │
└─────────────────────────────────────────────────────────────┘
```

**Current tools fail because**:
1. LLMs have context limits (128K-200K tokens max)
2. Simple concatenation creates monolithic blobs
3. No way to discover content in the middle/end of large files
4. RAG chunks lose semantic context
5. No unified search across all content

---

## The Solution: 5 Required Components

### Component 1: AST-Aware Semantic Chunking

**What it does**: Breaks files at natural boundaries (functions, classes) not arbitrary character counts.

```python
# WRONG: Arbitrary chunking
chunk_1 = content[0:2000]      # Might cut mid-function
chunk_2 = content[2000:4000]   # Loses context

# RIGHT: Semantic chunking
chunk_1 = lines[0:45]    # Complete class UserService
chunk_2 = lines[40:90]   # Complete function create_user (with overlap)
chunk_3 = lines[85:140]  # Complete function update_user (with overlap)
```

**Key properties**:
- Target: 1500 tokens per chunk (fits easily in any LLM)
- Max: 2000 tokens (hard limit)
- Overlap: 5-10 lines between chunks for continuity
- Boundaries: Function/class definitions, major comment blocks

---

### Component 2: Per-Chunk Metadata Sidecars

**What it does**: Every chunk gets a discoverable index entry.

```
.ai-index/chunks/
├── user_service_001.md      # Human-readable sidecar
├── user_service_001.json    # Machine-readable metadata
├── user_service_002.md
├── user_service_002.json
└── ...
```

**Sidecar content** (`user_service_002.json`):
```json
{
  "chunk_id": "user_service_002",
  "source_file": "src/services/user_service.py",
  "line_start": 45,
  "line_end": 95,
  "token_count": 1456,
  "symbols": [
    {"name": "create_user", "type": "function", "line": 47},
    {"name": "validate_user_data", "type": "function", "line": 78}
  ],
  "keywords": ["create", "user", "validation", "database", "email"],
  "summary": "User creation with validation logic"
}
```

**Why this matters**: AI can search these lightweight files to find relevant chunks without loading full content.

---

### Component 3: Multi-Level Hierarchy

**What it does**: Enables navigation from project → module → file → chunk.

```
.ai-index/
│
├── manifest.json           # Level 0: Project overview
│   └── "50 files, 127 chunks, 45K tokens total"
│
├── modules/                # Level 1: Folder summaries
│   ├── src.md              # "Source code root: api/, models/, services/"
│   ├── src_api.md          # "API layer: routes, handlers, middleware"
│   └── src_services.md     # "Business logic: user, order, payment"
│
├── files/                  # Level 2: File indexes
│   ├── user_service.json   # "3 chunks, exports: create_user, update_user..."
│   └── order_service.json
│
└── chunks/                 # Level 3: Individual chunks
    ├── user_service_001.json
    ├── user_service_002.json
    └── user_service_003.json
```

**Navigation flow**:
```
AI Question: "How does payment retry work?"
    ↓
1. Check modules/src_services.md → mentions "payment" 
2. Check files/payment_service.json → 5 chunks, has "retry" keyword
3. Check chunks/payment_service_003.json → lines 180-240, "retry" symbol
4. Read actual lines 180-240 from payment_service.py
```

---

### Component 4: Unified Search Indexes

**What it does**: Provides instant lookup without reading all sidecars.

**symbols.json** - Find any function/class:
```json
{
  "create_user": [
    {"file": "src/services/user_service.py", "line": 47, "type": "function"},
    {"file": "tests/test_user.py", "line": 12, "type": "function"}
  ],
  "retry_payment": [
    {"file": "src/services/payment_service.py", "line": 183, "type": "function"}
  ]
}
```

**keywords.json** - Find content by topic:
```json
{
  "validation": [
    {"chunk_id": "user_service_002", "file": "...", "lines": "45-95"},
    {"chunk_id": "order_service_001", "file": "...", "lines": "1-50"}
  ],
  "retry": [
    {"chunk_id": "payment_service_003", "file": "...", "lines": "180-240"}
  ]
}
```

**dependencies.json** - Understand code relationships:
```json
{
  "src/services/user_service.py": {
    "imports": ["models.User", "database.connection"],
    "imported_by": ["api/handlers/user_handler.py", "tests/test_user.py"]
  }
}
```

---

### Component 5: Content Hashing + Incremental Updates

**What it does**: Keeps index current without full regeneration.

```python
# On each indexing run:
for file in changed_files:
    new_hash = sha256(file.content)
    old_hash = index_db.get(file.path)
    
    if new_hash != old_hash:
        # Only reindex this file
        delete_old_chunks(file.path)
        create_new_chunks(file.path)
        update_search_indexes(file.path)
        index_db.set(file.path, new_hash)
```

**Result**: 5-second incremental update vs 5-minute full rebuild.

---

## Output Structure

```
project/
├── .ai-index/                          # AI-readable index
│   ├── manifest.json                   # Project stats + structure
│   ├── llms.txt                        # Human-readable overview
│   │
│   ├── modules/                        # Folder-level summaries
│   │   ├── root.md
│   │   ├── src.md
│   │   ├── src_api.md
│   │   └── src_services.md
│   │
│   ├── files/                          # File-level metadata
│   │   ├── user_service.py.json
│   │   ├── order_service.py.json
│   │   └── ...
│   │
│   ├── chunks/                         # Chunk-level detail
│   │   ├── user_service_001.md
│   │   ├── user_service_001.json
│   │   ├── user_service_002.md
│   │   ├── user_service_002.json
│   │   └── ...
│   │
│   └── search/                         # Unified search indexes
│       ├── symbols.json                # symbol → file:line
│       ├── keywords.json               # keyword → chunk_ids
│       └── dependencies.json           # import/export graph
│
└── src/                                # Original source (unchanged)
    ├── services/
    │   ├── user_service.py
    │   └── order_service.py
    └── api/
        └── handlers.py
```

---

## How AI Uses This

### Query: "Find the payment retry logic"

```
Step 1: Check search/keywords.json
        → "retry" → ["payment_service_003"]

Step 2: Read chunks/payment_service_003.json
        → source: payment_service.py, lines: 180-240
        → symbols: retry_payment, calculate_backoff
        → keywords: retry, payment, backoff, exponential

Step 3: Read actual content
        → file_read("src/services/payment_service.py", offset=180, limit=60)

Result: AI finds EXACT location in 3 steps, not scanning 5MB of text
```

---

## Comparison: Before vs After

| Scenario | Without Full Coverage | With Full Coverage |
|----------|----------------------|-------------------|
| 5MB codebase | Only first 128K tokens visible | 100% indexed in ~150 chunks |
| Finding function at line 5000 | Invisible to LLM | Found via symbols.json |
| Understanding dependencies | Must guess | Explicit in dependencies.json |
| Updating after changes | Full reindex | Incremental (seconds) |
| Finding by concept | Hope it's near top | keyword search |

---

## Usage

```bash
# Generate full coverage index
python tmp/full-coverage-indexer.py /path/to/project

# With custom chunk size
python tmp/full-coverage-indexer.py /path/to/project --chunk-size 1000

# Output to specific location
python tmp/full-coverage-indexer.py /path/to/project --output-dir ./my-index
```

---

## Key Guarantees

1. **Every line of code is in exactly one chunk** (with overlap for context)
2. **Every chunk is searchable by symbol name** via symbols.json
3. **Every chunk is searchable by keyword** via keywords.json  
4. **Every chunk has line range reference** to read original content
5. **No content is orphaned** - manifest tracks all files and chunks
