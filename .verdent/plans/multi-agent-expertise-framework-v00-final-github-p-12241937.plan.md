# Multi-Agent Expertise Framework v00 - Final GitHub Package

## Objective

Create the production-ready **multi-agent-expertise-framework** GitHub repository combining:

- **DOE Framework** (Directives → Orchestration → Execution)
- **Elle Context System** (9-layer context architecture)
- **Memory Operations System** (Two-tier: Global + Project)
- **7-Agent Pipeline** (MetaGPT orchestrator + 6 specialized agents)
- **5 Mental Models** (Garden, Budget, River, Biopsychosocial, Alchemy)
- **Self-Improving Expertise System** (4-pillar YAML + validation)

**GitHub URL**: `https://github.com/MartinMayday/multi-agent-expertise-framework`

---

## Complete Repository Structure

```
multi-agent-expertise-framework/
├── README.md                           # Project overview + quick start
├── AGENTS.md                           # Progressive disclosure index
├── CLAUDE.md                           # Global AI context (team-shared)
├── LICENSE                             # MIT
├── .gitignore                          # Python + secrets + .local
├── pyproject.toml                      # Python package config
├── requirements.txt                    # Dependencies
│
├── 0_directives/                       # DOE: THE WHAT
├── 1_orchestration/                    # DOE: THE WHO
├── 2_executions/                       # DOE: THE HOW
├── 3_state/                            # Memory Operations System
│
├── src/                                # Python implementation
├── __ref__/                            # Reference materials
├── demos/                              # Working examples
├── scripts/                            # Utility scripts
└── tests/                              # Test suite
```

---

## Phase 1: Directives Layer (`0_directives/`)

```
0_directives/
├── AGENTS.md                           # Directives layer index
├── README.md                           # How directives work
│
├── core/                               # Enforcement directives (from original)
│   ├── KB_GUARDRAILS.md               # KB-first execution protocol
│   ├── HANDOFF_PROTOCOL.md            # Agent state transfer
│   ├── PROGRESSIVE_LOADING.md         # Context management (L1-L4)
│   ├── FAILURE_HANDLING.md            # Graceful error handling
│   ├── STAGING_AND_APPROVAL.md        # Write validation policy
│   └── AGENT_HOOKS.md                 # Lifecycle hooks
│
├── policies/
│   ├── goals.md                       # Business/technical goals
│   ├── guardrails.md                  # ALWAYS/NEVER rules
│   └── security.md                    # Security constraints
│
├── workflows/                          # Workflow templates
│   ├── question.md                    # Q&A mode (MISSING - ADD)
│   ├── plan.md                        # Planning phase
│   ├── build.md                       # Implementation phase
│   ├── self-improve.md                # Self-annealing phase
│   └── plan_build_improve.md          # Complete 3-phase with TaskOutput gates
│
├── templates/
│   ├── expertise.yaml.example         # 4-pillar knowledge structure
│   ├── command.md.template            # Command template with sections
│   └── workflow.yaml.template         # Workflow schema
│
└── best-practices/                     # NEW: From original repo
    ├── correct-patterns.md            # ✅ What to do
    └── anti-patterns.md               # ❌ What NOT to do
```

### Key Additions from Original Repo:

**1. question.md Template** (Q&A with expertise validation):

```markdown
---
allowed-tools: Read, Grep, Glob
argument-hint: [question]
---
# Purpose: Answer questions using expertise with codebase validation

## Variables
- USER_QUESTION: $1

## Instructions
- CRITICAL: Always validate expertise against codebase
- Expertise files are NOT authoritative - the codebase is

## Workflow
1. Read expertise.yaml
2. Search codebase to validate expertise claims
3. Identify discrepancies
4. Answer with validated information
5. Flag outdated expertise for self-improve

## Report
- Answer with source references
- Discrepancies identified
- Expertise update recommendations
```

**2. TaskOutput Gates Pattern** (plan_build_improve.md):

```
CRITICAL: DO NOT STOP between steps - continue through all steps

Step 1: Task() → TaskOutput(path_to_plan)
        ↓ RETRIEVE TaskOutput BEFORE proceeding
Step 2: Task() → TaskOutput(build_report)
        ↓ RETRIEVE TaskOutput BEFORE proceeding
Step 3: Task() → TaskOutput(self_improve_report)
        ↓ RETRIEVE TaskOutput BEFORE proceeding
Step 4: Task() → TaskOutput(path_to_report)

Key Learning: Subagents start fresh with no prior context.
Each step is independent and MUST retrieve previous output.
```

**3. Required Command Sections**:

- `# Purpose` - What this command does
- `## Variables` - Named inputs (e.g., USER_QUESTION: $1)
- `## Instructions` - Constraints and rules
- `## Workflow` - Step-by-step execution
- `## Report` - Expected output format
- `Use example:` - Usage demonstration

---

## Phase 2: Orchestration Layer (`1_orchestration/`)

```
1_orchestration/
├── AGENTS.md                           # Orchestration layer index
├── orchestrator.py                     # DOE orchestrator (stub)
├── context_loader.py                   # Progressive disclosure (stub)
│
├── mental_models/                      # 5 Cognitive frameworks
│   ├── README.md                       # Mental models index
│   ├── 01_garden_model.md             # Cultivation metaphor
│   ├── 02_budget_model.md             # Resource allocation
│   ├── 03_river_model.md              # Flow dynamics
│   ├── 04_biopsychosocial_model.md    # Multi-dimensional
│   └── 05_alchemy_model.md            # Transformation
│
├── knowledge/
│   ├── skills/                         # Anthropic Skills pattern
│   │   ├── README.md
│   │   ├── research-specialist/SKILL.md
│   │   ├── code-analyst/SKILL.md
│   │   └── devops-engineer/SKILL.md
│   └── expertise/
│       └── README.md                  # Populated via self-improve
│
├── agents/                             # 7-Agent Pipeline
│   ├── README.md                       # Agent architecture
│   ├── AGENTS_CATALOG.md              # Agent registry
│   │
│   ├── metagpt/                        # Orchestrator
│   │   ├── metagpt_system-instructions.md
│   │   ├── kb_metagpt-manifest.md
│   │   ├── mcp.json
│   │   └── .env.example
│   ├── researchgpt/                    # Research (web.search, web.scrape)
│   ├── analysisgpt/                    # Analysis (no tools)
│   ├── designgpt/                      # Design (no tools)
│   ├── implementationgpt/              # Code (Write, Read, Bash)
│   ├── testgpt/                        # Testing (Bash, Read)
│   ├── evaluationgpt/                  # Evaluation (Read, Write reports)
│   │
│   └── interfaces/                     # Pluggable adapters
│       ├── base_agent.py              # Abstract interface
│       ├── agent_registry.py
│       └── adapters/
│           ├── pydantic_ai.py         # Stub
│           ├── crew_ai.py             # Stub
│           ├── autogen.py             # Stub
│           └── claude_flow.py         # Stub
│
└── invocation/                         # NEW: Invocation patterns
    ├── command_pattern.md             # /experts:<domain>:<action> [args]
    └── agent_pattern.md               # @agent-<name> [prompt]
```

### Invocation Patterns (from original):

**Command Pattern**:

```
/experts:<domain>:<action> [arguments]

Examples:
- /experts:database:question "How does information flow?"
- /experts:websocket:plan "Add session counter"
- /experts:api:plan_build_improve "Implement auth"
```

**Agent Pattern**:

```
@agent-<name> [prompt]

Examples:
- @agent-planner create a plan for feature X
- @agent-meta-agent create a database expert agent
- @agent-database-expert How does our schema work?
```

---

## Phase 3: Executions Layer (`2_executions/`)

```
2_executions/
├── AGENTS.md                           # Executions layer index
├── README.md
│
├── tools/
│   ├── README.md
│   ├── example_tool.py                # Working demo
│   └── context_generator/             # Production tool (from tmp/)
│
├── workflows/
│   ├── plan.py                        # Planning workflow
│   ├── build.py                       # Build workflow
│   └── plan_build_improve.py          # Chained with TaskOutput gates
│
├── utils/
│   ├── providers.py                   # Multi-provider LLM interface
│   ├── context_manager.py             # Context handling
│   ├── error_handler.py               # Error recovery
│   └── retry.py                       # NEW: Autonomous retry logic
│
└── eval/
    └── eval_plan.py
```

### Autonomous Retry Configuration (from G3):

```python
# retry.py
RETRY_CONFIG = {
    "default_mode": 3,
    "autonomous_mode": 6,
    "base_delays": [10, 30, 60, 120, 180, 200],  # 600s total
    "jitter": 0.30,  # ±30%
    "recoverable_errors": [
        "RateLimitError",
        "NetworkError",
        "ServerError",
        "ModelBusy",
        "Timeout"
    ]
}
# NOT exponential backoff - fixed intervals with jitter distribution
```

---

## Phase 4: Memory Operations System (`3_state/`)

From `.verdent/plans/memory-operations-system-implementation-plan-12241927.plan.md`:

```
3_state/                                # Memory Operations System
├── AGENTS.md                           # State layer index
├── CLAUDE.md                           # Elle-style instructions
├── context-update.md                   # How to update memory
│
├── 00_rules/                           # Immutable context (Constitution)
│   ├── project.md                     # Project mission & architecture
│   ├── style_guide.md                 # Coding conventions
│   └── team.md                        # Team roles & protocols
│
├── 01_state/                           # Operational memory
│   ├── active_session.json            # Current session metadata
│   ├── task_queue.json                # DOE task state
│   └── scratchpad.md                  # Agent shared whiteboard
│
├── 02_memory/                          # Learning layer (Self-annealing)
│   ├── decisions.log.md               # ADR-style decision log
│   ├── patterns.md                    # Learned patterns
│   ├── entities.json                  # Named entities
│   └── learned_facts.ndjson           # Extracted facts (append-only)
│
└── 03_archive/                         # Historical layer
    └── sessions/
        └── .gitkeep
```

### Global Memory Location:

```
~/.expert-framework/                    # User-scoped (NOT in repo)
├── profile.json                       # User identity
├── preferences.md                     # Personal preferences
├── global_rules.md                    # Cross-project rules
├── learned_facts.ndjson               # Global facts
├── patterns.md                        # Global patterns
└── tools/                             # Tool configs
```

---

## Phase 5: Source Implementation (`src/`)

```
src/
├── __init__.py
├── schemas/                            # JSON Schema validation
│   ├── profile.schema.json
│   ├── session.schema.json
│   ├── task_queue.schema.json
│   ├── fact.schema.json
│   └── entity.schema.json
│
├── memory/                             # Memory Operations
│   ├── __init__.py
│   ├── context_manager.py             # Path resolution, load/save
│   ├── event_logger.py                # NDJSON append-only logging
│   ├── task_queue.py                  # DOE task state CRUD
│   ├── fact_extractor.py              # Triplet extraction
│   └── pattern_recognizer.py          # Pattern detection
│
├── agents/
│   └── reflector.py                   # Post-execution analysis
│
├── scaffold/
│   └── project_context.py             # .context/ generator
│
├── cli/
│   └── memory.py                      # CLI commands
│
└── agentic_os/                         # Core library (from scaffold)
    ├── __init__.py
    ├── paths.py
    ├── render.py
    └── checks.py
```

### CLI Commands:

```bash
expert memory init      # Create .context/ in current directory
expert memory status    # Show active session, task queue, blockers
expert memory clear     # Archive and reset 01_state/
expert memory search    # BM25 search across 02_memory/ and 03_archive/
expert memory summarize # Generate session summary from logs
```

---

## Phase 6: Reference Materials (`__ref__/`)

```
__ref__/
├── README.md
├── mental-models/                      # (linked to 1_orchestration/)
├── context-templates/
│   ├── schema_template.yaml
│   └── minimal_context.yaml
├── framework-comparisons/
│   ├── pydantic-ai.md
│   ├── crew-ai.md
│   ├── autogen.md
│   └── langgraph.md
├── doe-framework/
├── elle-context-system/
└── expert-framework-drafts/            # Original reverse-engineered artifacts
    ├── README.md
    ├── SUMMARY.md
    ├── GAP_ANALYSIS.md
    ├── PRODUCTION_ROADMAP.md
    └── __ref/                          # FRAMEWORK.md, synthesis docs
```

---

## Phase 7: Demos

```
demos/
├── README.md
├── 01-simple-directive/
├── 02-context-loading/
├── 03-agent-handoff/
├── 04-plan-build-improve/              # TaskOutput gates demo
└── 05-expertise-validation/            # Codebase validation demo
```

---

## Files to Migrate

| Source | Target | Action |
| --- | --- | --- |
| `__ref/expert-framework-reverse-engineered-drafts/directives/` | `0_directives/` | Restructure |
| `__ref/expert-framework-reverse-engineered-drafts/agents/` | `1_orchestration/agents/` | Copy |
| `__ref/context-engineering-frameworks/.../10_mental_models/` | `1_orchestration/mental_models/` | Copy |
| `__ref/expert-framework-reverse-engineered-drafts/original-repo/tmp/...` | `0_directives/workflows/` | Merge templates |
| `tmp/context_generator/` | `2_executions/tools/context_generator/` | Copy |
| `.verdent/plans/memory-operations-system-*.plan.md` | `3_state/` structure | Implement |

---

## Verification Criteria

| Phase | Verification |
| --- | --- |
| Phase 1 | All core directives present; question.md exists; best-practices/ populated |
| Phase 2 | 5 mental models present; 7 agents with system-instructions; invocation docs |
| Phase 3 | context_generator importable; retry.py with config |
| Phase 4 | .context/ scaffold creates all subdirs; 00_rules through 03_archive |
| Phase 5 | JSON schemas validate; CLI commands execute |
| Phase 6 | Framework comparisons present; original artifacts archived |
| Phase 7 | Demo 04 demonstrates TaskOutput gates |

---

## Step → Targets → Verification

| Step | Targets | Verification |
| --- | --- | --- |
| 1 | Create root structure | All directories exist |
| 2 | Create `0_directives/` | Core + question.md + best-practices |
| 3 | Create `1_orchestration/` | Mental models + 7 agents + invocation |
| 4 | Create `2_executions/` | Tools + retry.py |
| 5 | Create `3_state/` | 00-03 subdirs + schemas |
| 6 | Create `src/` | Memory components + CLI |
| 7 | Organize `__ref__/` | Comparisons + originals |
| 8 | Create demos | 5 demos including TaskOutput |
| 9 | Git init + push | GitHub repo created |

---

## Constraints

- **Python 3.11+** compatibility
- **File-based only** (no external databases)
- **Progressive disclosure** (L1-L4 loading)
- **Two-tier memory**: Global (`~/.expert-framework/`) + Project (`3_state/`)
- **TaskOutput gates** enforced in chained workflows
- **Expertise validation**: Codebase is authoritative, not expertise.yaml
- **Git-friendly**: 3_state/ committed, \~/.expert-framework/ local-only

---

## Post-Implementation

1. `git init` in repository root
2. Create GitHub repo: `MartinMayday/multi-agent-expertise-framework`
3. `git remote add origin git@github.com:MartinMayday/multi-agent-expertise-framework.git`
4. `git add . && git commit -m "feat: Initial v00 multi-agent expertise framework"`
5. `git push -u origin main`
6. Create GitHub release v0.1.0