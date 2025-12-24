# v00 Remediation: Context Rot Fixes and Missing Components

## Objective

Fix the 7 critical issues in the v00 Multi-Agent Expertise Framework:

1. Remove `__ref__` from inside v00 folder
2. Clean root directory clutter (duplicate directories, files with spaces)
3. Implement full Memory Operations System per approved plan
4. Archive GPT agents (replace with multi-agent framework stubs)
5. Add default reference expertise agents
6. Verify and fix GitHub commit state
7. Create Framework Definition Blueprint

---

## Issue Analysis

| \# | Issue | Current State | Required State |
| --- | --- | --- | --- |
| 1 | `__ref__` inside v00 | `v00/__ref__/` exists | v00 is self-contained, no `__ref__` inside |
| 2 | Root clutter | 38+ items including duplicates | Clean: only `.verdent/`, `v00/`, `archived/`, `.git` |
| 3 | Memory Ops incomplete | Only `context_manager.py` + 2 schemas | Full Phase 1-5 from plan |
| 4 | GPT agents present | `1_orchestration/agents/metagpt/`, etc. | Archived; stub interfaces for future frameworks |
| 5 | Missing expertise agents | None | Default expertise.yaml + knowledge/skills structure |
| 6 | GitHub state | Committed with flawed structure | Clean commit with corrected v00 |
| 7 | No framework blueprint | Missing | `FRAMEWORK.md` explaining what/why/how |

---

## Phase 1: Clean Repository Structure

### Step 1.1: Remove `__ref__` from v00

**Target**: `v00-multi-agent-expertise-framework/`

**Actions**:

- Delete `v00-multi-agent-expertise-framework/__ref__/` directory
- v00 must be self-contained production code only

### Step 1.2: Clean Root Directory

**Target**: Repository root `/th_agent-EXPERT-framework/`

**Final root structure**:

```
/th_agent-EXPERT-framework/
├── .git/
├── .verdent/                    # Keep: plan history
├── v00-multi-agent-expertise-framework/  # ONLY production code
└── __ref/                       # Keep: reference materials (renamed from __ref__)
```

**To archive/delete**:

| Item | Action |
| --- | --- |
| Directories with spaces (`, `**ref**\`, etc.) | Delete (artifacts) |
| Root `0_directives/`, `1_orchestration/`, `2_executions/`, `3_state/` | Delete (duplicates of v00) |
| Root `src/`, `demos/`, `scripts/` | Delete (duplicates of v00) |
| `__ref__/` (duplicate of `__ref`) | Delete |
| `staging/`, `tests/`, `tmp/` | Archive to `__ref/archived/` |
| `archived/` | Move to `__ref/archived/` |
| `AGENTS-CATALOG.md`, `FRAMEWORK-CHECKLIST.md` | Move to `__ref/analysis/` |
| `.ck/`, `.ckignore`, `.cursorindexingignore`, `.specstory/` | Keep (tool configs) |

---

## Phase 2: Complete Memory Operations System

### Step 2.1: Create Missing src/ Components

**Target**: `v00/src/memory/`

**Files to create**:

| File | Purpose |
| --- | --- |
| `event_logger.py` | NDJSON append-only session logging |
| `task_queue.py` | DOE task state CRUD |
| `fact_extractor.py` | Triplet extraction from logs |
| `pattern_recognizer.py` | Heuristic pattern detection |

**Target**: `v00/src/agents/`

| File | Purpose |
| --- | --- |
| `reflector.py` | Post-execution analysis agent |

**Target**: `v00/src/scaffold/`

| File | Purpose |
| --- | --- |
| `project_context.py` | `.context/` scaffold generator |

### Step 2.2: Create Missing Schemas

**Target**: `v00/src/schemas/`

| File | Status |
| --- | --- |
| `profile.schema.json` | **CREATE** |
| `session.schema.json` | Exists |
| `task_queue.schema.json` | Exists |
| `fact.schema.json` | **CREATE** |
| `entity.schema.json` | **CREATE** |

### Step 2.3: Complete 3_state Structure

**Target**: `v00/3_state/`

**Required structure**:

```
3_state/
├── 00_rules/
│   ├── project.md         # Exists
│   ├── style_guide.md     # CREATE
│   └── team.md            # CREATE
├── 01_state/
│   ├── active_session.json  # CREATE
│   ├── task_queue.json      # Exists
│   └── scratchpad.md        # CREATE
├── 02_memory/
│   ├── decisions.log.md     # CREATE
│   ├── patterns.md          # CREATE
│   └── entities.json        # CREATE
└── 03_archive/
    └── sessions/
        └── .gitkeep         # CREATE
```

---

## Phase 3: Archive GPT Agents, Add Framework Stubs

### Step 3.1: Archive GPT Agent Definitions

**Target**: `v00/1_orchestration/agents/`

**Actions**:

- Move `metagpt/`, `researchgpt/`, `analysisgpt/`, `designgpt/`, `implementationgpt/`, `testgpt/`, `evaluationgpt/` to `__ref/archived/gpt-agent-definitions/`

### Step 3.2: Create Multi-Agent Framework Stubs

**Target**: `v00/1_orchestration/agents/`

**New structure**:

```
1_orchestration/agents/
├── README.md              # Agent architecture overview
├── interfaces/
│   ├── __init__.py
│   ├── base_agent.py      # Abstract interface
│   └── agent_registry.py  # Agent discovery
└── adapters/
    ├── __init__.py
    ├── pydantic_ai.py     # Stub: PydanticAI adapter
    ├── crew_ai.py         # Stub: CrewAI adapter
    ├── claude_flow.py     # Stub: Claude-flow adapter
    ├── praison_ai.py      # Stub: PraisonAI adapter
    └── claude_sdk.py      # Stub: Claude Agent SDK adapter
```

### Step 3.3: Create Default Reference Expertise

**Target**: `v00/1_orchestration/knowledge/`

**Structure**:

```
1_orchestration/knowledge/
├── README.md
├── skills/
│   ├── README.md
│   ├── research-specialist/
│   │   └── SKILL.md
│   ├── code-analyst/
│   │   └── SKILL.md
│   └── devops-engineer/
│       └── SKILL.md
└── expertise/
    ├── README.md
    └── framework.expertise.yaml  # Default expertise template
```

`framework.expertise.yaml` **structure** (4-pillar):

```yaml
# Identity
name: framework-expert
version: "0.1.0"
domain: multi-agent-expertise-framework

# Context
mental_models:
  - garden    # Cultivation metaphor
  - budget    # Resource allocation
  - river     # Flow dynamics
  - biopsychosocial  # Multi-dimensional
  - alchemy   # Transformation

# Knowledge (populated by self-improve)
concepts: []
patterns: []
entities: []

# Behavior
workflows:
  - question
  - plan
  - build
  - self-improve
  - plan_build_improve
```

---

## Phase 4: Create Framework Blueprint

### Step 4.1: Create FRAMEWORK.md

**Target**: `v00/FRAMEWORK.md`

**Contents**:

1. **What is it**: Multi-agent expertise OS combining DOE + Elle Context + Self-Improvement
2. **Architecture**: DOE layers (0_directives → 1_orchestration → 2_executions) + Memory (3_state)
3. **Key Concepts**:
   - Progressive Disclosure (L1-L4)
   - TaskOutput Gates
   - Expertise Validation (codebase is authoritative)
   - Self-Annealing (facts → patterns)
4. **Invocation Patterns**: `/experts:<domain>:<action>` + `@agent-<name>`
5. **Mental Models**: 5 cognitive frameworks
6. **Multi-Agent Integration**: Pluggable adapters for PydanticAI/CrewAI/etc.
7. **Getting Started**: Quick setup and first workflow

### Step 4.2: Update README.md

**Target**: `v00/README.md`

- Add link to FRAMEWORK.md
- Update Quick Start to reflect actual CLI commands
- Add architecture diagram (ASCII or Mermaid)

---

## Phase 5: Git Cleanup and Push

### Step 5.1: Stage and Commit

**Actions**:

1. `git add -A`
2. Commit message:

   ```
   fix: Remediate v00 structure and complete Memory Ops System
   
   - Remove __ref__ from v00 (production-only folder)
   - Clean root directory clutter
   - Implement full Memory Ops System (Phase 1-5 from plan)
   - Archive GPT agents, add multi-agent framework stubs
   - Add default reference expertise (skills + expertise.yaml)
   - Create FRAMEWORK.md blueprint
   ```

### Step 5.2: Push to GitHub

```bash
git push origin main
```

---

## Verification Criteria (Definition of Done)

| Phase | Verification |
| --- | --- |
| Phase 1 | Root has only `.git/`, `.verdent/`, `v00/`, `__ref/`, tool configs; v00 has no `__ref__` inside |
| Phase 2 | All 6 `src/memory/*.py` files exist; 5 schemas exist; `3_state/` has 00-03 subdirs with required files |
| Phase 3 | No GPT agent folders in v00; `1_orchestration/agents/interfaces/` and `adapters/` exist; `knowledge/skills/` has 3 specialists |
| Phase 4 | `FRAMEWORK.md` exists with 7 sections; `README.md` links to it |
| Phase 5 | `git status` clean; `git log -1` shows remediation commit; GitHub repo updated |

---

## Step → Targets → Verification

| Step | Target Files/Dirs | Verification |
| --- | --- | --- |
| 1.1 | `v00/__ref__/` | Directory deleted |
| 1.2 | Repository root | `ls` shows only allowed items |
| 2.1 | `v00/src/memory/*.py` | 6 Python files exist, syntax valid |
| 2.2 | `v00/src/schemas/*.json` | 5 JSON schemas exist, valid JSON |
| 2.3 | `v00/3_state/0[0-3]_*/` | All subdirs + files exist |
| 3.1 | `__ref/archived/gpt-agent-definitions/` | 7 GPT agent dirs moved |
| 3.2 | `v00/1_orchestration/agents/` | `interfaces/`, `adapters/` with stubs |
| 3.3 | `v00/1_orchestration/knowledge/` | 3 skills + expertise.yaml |
| 4.1 | `v00/FRAMEWORK.md` | File exists with 7 sections |
| 4.2 | `v00/README.md` | Links to FRAMEWORK.md |
| 5.1-5.2 | `.git/` | Clean status, pushed to origin |

---

## Constraints

- **No breaking changes**: Existing workflows in 40-workflows must remain functional
- **File-based only**: No external databases
- **Python 3.11+**: All new code compatible
- **Git-friendly**: 3_state/ committed; \~/.expert-framework/ local-only