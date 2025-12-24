## Objective

Implement a **File-Based Memory Operations System** for the Expert Framework that extends Elle's personal context into a comprehensive operational memory platform with **Global (user)** and **Project (team/agent)** scopes.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     MEMORY OPERATIONS SYSTEM                     │
├─────────────────────────────────────────────────────────────────┤
│  GLOBAL SCOPE (~/.expert-framework/)                            │
│  ├── profile.json          # User identity (Elle: identity.md)  │
│  ├── preferences.md        # User preferences (Elle layer)      │
│  ├── global_rules.md       # Cross-project directives           │
│  ├── learned_facts.ndjson  # Extracted user facts (Zep-style)   │
│  ├── patterns.md           # Self-annealed heuristics           │
│  └── tools/                # Global tool configs                │
├─────────────────────────────────────────────────────────────────┤
│  PROJECT SCOPE (<repo>/.context/)                               │
│  ├── 00_rules/             # Immutable context (Constitution)   │
│  ├── 01_state/             # Operational memory (JSON/MD)       │
│  ├── 02_memory/            # Learning layer (Facts/Patterns)    │
│  └── 03_archive/           # Historical layer (Sessions/Logs)   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Directory Structure & Schemas

### Step 1.1: Create Global Memory Scaffold

**Target**: `~/.expert-framework/`

```
~/.expert-framework/
├── profile.json              # User identity schema
├── preferences.md            # Markdown preferences (Elle-style)
├── global_rules.md           # Cross-project rules
├── learned_facts.ndjson      # Empty, append-only facts log
├── patterns.md               # Empty patterns template
└── tools/
    └── .gitkeep
```

**Files to Create**:

| File | Format | Purpose |
| --- | --- | --- |
| `profile.json` | JSON | `{id, name, email, timezone, consent_flags, created_at}` |
| `preferences.md` | Markdown | Communication style, output preferences |
| `global_rules.md` | Markdown | "Always use TypeScript", "Never use localhost" |
| `learned_facts.ndjson` | NDJSON | Empty file for fact extraction |
| `patterns.md` | Markdown | Template with `## Known Patterns` heading |

### Step 1.2: Create Project Memory Scaffold Generator

**Target**: `src/scaffold/project_context.py`

Creates `.context/` structure in any repository:

```
.context/
├── 00_rules/
│   ├── project.md            # Project mission & architecture
│   ├── style_guide.md        # Coding conventions
│   └── team.md               # Team roles & protocols
├── 01_state/
│   ├── active_session.json   # Current session metadata
│   ├── task_queue.json       # DOE task state
│   └── scratchpad.md         # Agent shared whiteboard
├── 02_memory/
│   ├── decisions.log.md      # ADR-style decision log
│   ├── patterns.md           # Project-specific patterns
│   └── entities.json         # Named entities (servers, APIs)
└── 03_archive/
    └── sessions/
        └── .gitkeep
```

### Step 1.3: Define JSON Schemas

**Target**: `src/schemas/`

| Schema File | Purpose |
| --- | --- |
| `profile.schema.json` | Global user profile validation |
| `session.schema.json` | `{id, goal, start_time, status, agent, step}` |
| `task_queue.schema.json` | `{tasks: [{id, content, status, blockers, created_at}]}` |
| `fact.schema.json` | `{id, subject, predicate, object, confidence, source, valid_at}` |
| `entity.schema.json` | `{name, type, value, description, last_verified}` |

---

## Phase 2: Core Components

### Step 2.1: ContextManager Class

**Target**: `src/memory/context_manager.py`

Responsibilities:

- Resolve paths for Global vs Project scope
- Load/save JSON and Markdown files
- Handle XDG fallbacks on macOS/Linux

Key Methods:

```python
class ContextManager:
    def get_global_path(self, filename: str) -> Path
    def get_project_path(self, filename: str) -> Path
    def load_rules(self) -> dict  # Merge global + project rules
    def load_session(self) -> dict
    def save_session(self, data: dict) -> None
```

### Step 2.2: EventLogger Class

**Target**: `src/memory/event_logger.py`

Responsibilities:

- Append-only NDJSON streaming
- Session event capture (tool calls, decisions, errors)
- Atomic writes with fsync

Key Methods:

```python
class EventLogger:
    def log_event(self, event_type: str, payload: dict) -> None
    def log_tool_call(self, tool: str, args: dict, result: dict) -> None
    def log_decision(self, decision: str, rationale: str) -> None
    def get_session_log_path(self) -> Path
```

### Step 2.3: TaskQueue Manager

**Target**: `src/memory/task_queue.py`

Responsibilities:

- CRUD for DOE task states
- Status transitions (pending → in_progress → completed/blocked)
- Blocker tracking

Key Methods:

```python
class TaskQueue:
    def add_task(self, content: str, priority: int = 0) -> str
    def update_status(self, task_id: str, status: str) -> None
    def get_active_task(self) -> dict | None
    def get_blocked_tasks(self) -> list[dict]
```

---

## Phase 3: Self-Annealing (Learning Layer)

### Step 3.1: FactExtractor Class

**Target**: `src/memory/fact_extractor.py`

Responsibilities:

- Parse session logs for extractable facts
- Generate triplets: `(Subject, Predicate, Object)`
- Assign confidence scores

Key Methods:

```python
class FactExtractor:
    def extract_from_log(self, log_path: Path) -> list[Fact]
    def extract_entities(self, text: str) -> list[Entity]
    def promote_fact(self, fact: Fact, scope: Literal["global", "project"]) -> None
```

### Step 3.2: PatternRecognizer Class

**Target**: `src/memory/pattern_recognizer.py`

Responsibilities:

- Detect repeated failures/successes
- Generate heuristic rules
- Update `patterns.md`

Key Methods:

```python
class PatternRecognizer:
    def analyze_session(self, session_log: Path) -> list[Pattern]
    def should_promote(self, pattern: Pattern) -> bool  # 2+ occurrences
    def write_pattern(self, pattern: Pattern, scope: str) -> None
```

### Step 3.3: Reflector Agent Integration

**Target**: `src/agents/reflector.py`

Responsibilities:

- Run post-execution analysis
- Orchestrate FactExtractor + PatternRecognizer
- Generate session summaries

Trigger: Called by DOE Orchestrator after task completion.

---

## Phase 4: DOE Integration

### Step 4.1: Modify Orchestrator Load Phase

**Target**: `src/orchestrator.py` (or equivalent DOE entry point)

Add to initialization:

```python
context = ContextManager()
rules = context.load_rules()  # Merge global + project
session = context.load_session()
# Inject into agent system prompt
```

### Step 4.2: Modify Execution Phase

**Target**: Execution loop

Add event logging:

```python
logger = EventLogger(context.get_project_path("03_archive/sessions"))
# Before each tool call:
logger.log_tool_call(tool_name, args, result)
```

### Step 4.3: Add Post-Execution Hook

**Target**: DOE completion handler

```python
# After task success/failure:
reflector = ReflectorAgent(context)
reflector.analyze_and_learn(session_id)
```

---

## Phase 5: CLI Commands

### Step 5.1: Memory CLI

**Target**: `src/cli/memory.py`

| Command | Action |
| --- | --- |
| `expert memory init` | Create `.context/` in current directory |
| `expert memory status` | Show active session, task queue, blockers |
| `expert memory clear` | Archive and reset `01_state/` |
| `expert memory search <query>` | BM25 search across `02_memory/` and `03_archive/` |
| `expert memory summarize` | Generate session summary from logs |

---

## Verification Criteria (Definition of Done)

| Phase | Verification |
| --- | --- |
| Phase 1 | `~/.expert-framework/` exists with valid `profile.json`; `.context/` generator creates all subdirectories |
| Phase 2 | Unit tests pass for ContextManager, EventLogger, TaskQueue; NDJSON appends are atomic |
| Phase 3 | FactExtractor produces valid triplets from sample logs; PatternRecognizer detects 2+ occurrence patterns |
| Phase 4 | DOE Orchestrator loads merged rules; EventLogger captures tool calls; Reflector runs on completion |
| Phase 5 | CLI commands execute without error; `expert memory init` creates valid scaffold |

---

## Step → Targets → Verification Traceability

| Step | Target Files | Verification |
| --- | --- | --- |
| 1.1 | `~/.expert-framework/*` | Directory exists, JSON validates |
| 1.2 | `src/scaffold/project_context.py` | `expert memory init` creates `.context/` |
| 1.3 | `src/schemas/*.json` | jsonschema validates sample data |
| 2.1 | `src/memory/context_manager.py` | Unit tests: path resolution, load/save |
| 2.2 | `src/memory/event_logger.py` | Unit tests: NDJSON append, fsync |
| 2.3 | `src/memory/task_queue.py` | Unit tests: CRUD, status transitions |
| 3.1 | `src/memory/fact_extractor.py` | Unit tests: triplet extraction |
| 3.2 | `src/memory/pattern_recognizer.py` | Unit tests: pattern detection |
| 3.3 | `src/agents/reflector.py` | Integration test: post-session analysis |
| 4.1-4.3 | `src/orchestrator.py` | Integration test: full DOE loop with logging |
| 5.1 | `src/cli/memory.py` | CLI smoke tests |

---

## Constraints & Dependencies

- **No External Databases**: File-based only (JSON, NDJSON, Markdown)
- **Git-Friendly**: `.context/` is committed; `~/.expert-framework/` is local-only
- **Progressive Disclosure**: Only `00_rules/` and `01_state/` loaded by default
- **Security**: No secrets in memory files; reference by ENV var name only
- **Stack**: Python 3.11+, pydantic for validation, typer for CLI

---

## Files to Create (Summary)

```
src/
├── schemas/
│   ├── profile.schema.json
│   ├── session.schema.json
│   ├── task_queue.schema.json
│   ├── fact.schema.json
│   └── entity.schema.json
├── memory/
│   ├── __init__.py
│   ├── context_manager.py
│   ├── event_logger.py
│   ├── task_queue.py
│   ├── fact_extractor.py
│   └── pattern_recognizer.py
├── agents/
│   └── reflector.py
├── scaffold/
│   └── project_context.py
└── cli/
    └── memory.py
```