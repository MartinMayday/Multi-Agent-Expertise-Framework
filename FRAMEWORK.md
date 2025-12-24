# Multi-Agent Expertise Framework v0.1.0

Production-ready agentic OS combining DOE, Elle Context, and Self-Improvement.

---

## 1. What Is It?

The **Multi-Agent Expertise Framework** is a file-based operating system for autonomous AI/LLM workers that separates concerns into three layers:

| Layer | Purpose | Location |
|-------|---------|----------|
| **Directives (The WHAT)** | Goals, policies, guardrails, workflows | `0_directives/` |
| **Orchestration (The WHO)** | Agent personas, mental models, skills | `1_orchestration/` |
| **Execution (The HOW)** | Tools, utilities, scripts | `2_executions/` |
| **Memory (LEARNING)** | Facts, patterns, decisions, sessions | `3_state/` |

This is the **DOE Architecture** (Directives → Orchestration → Execution) applied to multi-agent systems.

---

## 2. Key Concepts

### Progressive Disclosure (L1-L4)
Context is loaded in layers to optimize token usage:

- **L1 (Minimal)**: Goal, current step, blockers (~250 tokens)
- **L2 (Domain)**: Domain-specific metadata (~1000 tokens)
- **L3 (Task)**: Rich task context (~3000 tokens)
- **L4 (Full)**: All available context (~unlimited)

### Expertise Validation
The codebase is the source of truth. Expertise files (`expertise.yaml`) must be validated against actual implementation.

### Self-Annealing (Learning)
Post-execution analysis extracts:
- **Facts**: (Subject, Predicate, Object) triplets with confidence
- **Patterns**: Repeated behaviors, errors, success cases
- **Decisions**: ADR-style architectural decisions

### TaskOutput Gates
Multi-step workflows enforce sequential execution:
```
Step 1: Task() → TaskOutput(result1)
        ↓ RETRIEVE result1 BEFORE proceeding
Step 2: Task() → TaskOutput(result2)
        ↓ RETRIEVE result2 BEFORE proceeding
Step 3: Task() → TaskOutput(result3)
```

This ensures agents start fresh with complete context, avoiding hallucination.

---

## 3. Architecture

### Directory Structure

```
/
├── 0_directives/            # THE WHAT
│   ├── 00-meta/            # Meta-documentation
│   ├── 10-global/          # Global policies, guardrails
│   ├── 20-roles/           # Agent persona contracts
│   ├── 30-tools/           # Tool governance
│   ├── 40-workflows/       # Workflow templates (question, plan, build, improve)
│   ├── 50-templates/       # Reusable templates
│   └── 90-output-contracts/# Quality gates
│
├── 1_orchestration/         # THE WHO
│   ├── agents/
│   │   ├── interfaces/      # Base agent class
│   │   ├── adapters/        # PydanticAI, CrewAI, Claude SDK, etc. stubs
│   │   └── README.md        # Agent architecture
│   ├── mental_models/       # 5 cognitive frameworks
│   ├── invocation/          # /experts:domain:action patterns
│   └── knowledge/
│       ├── skills/          # Reusable expertise (research, code, devops)
│       └── expertise/       # Domain expertise.yaml files
│
├── 2_executions/            # THE HOW
│   ├── tools/              # Reusable tools
│   ├── workflows/          # Python implementations of workflows
│   └── utils/              # Retry logic, error handling
│
├── 3_state/                # MEMORY (Learning)
│   ├── 00_rules/           # Immutable: project constitution
│   ├── 01_state/           # Ephemeral: session state, task queue
│   ├── 02_memory/          # Append-only: facts, patterns, decisions
│   └── 03_archive/         # Historical: session logs
│
├── src/                    # Python implementation
│   ├── memory/             # ContextManager, EventLogger, FactExtractor, etc.
│   ├── agents/             # ReflectorAgent
│   ├── scaffold/           # .context/ generator
│   ├── cli/                # CLI commands
│   └── schemas/            # JSON schemas for validation
│
├── __ref__/                # Reference materials and artifacts
├── archived/               # Legacy files
├── demos/                  # Working examples
├── tests/                  # Test suite
├── staging/                # Empty (for testing)
└── tmp/                    # Non-critical temporary files
```

### Two-Tier Memory

**Global** (~/.expert-framework/):
- User identity, preferences
- Cross-project rules, patterns
- Local-only (NOT in Git)

**Project** (3_state/):
- Constitution, style guides
- Session state, task queue
- Facts, patterns, decisions
- Committed to Git

---

## 4. Invocation Patterns

### Command Pattern: `/experts:<domain>:<action> [arguments]`

```bash
/experts:database:question "How does our schema work?"
/experts:websocket:plan "Add session counter"
/experts:api:plan_build_improve "Implement auth"
/experts:framework:self-improve
```

### Agent Pattern: `@agent-<name> [prompt]`

```bash
@agent-research Investigate competing AI frameworks
@agent-planner Create a sprint plan
@agent-coder Implement user authentication
```

---

## 5. Mental Models

Five cognitive frameworks guide expertise:

| Model | Metaphor | Use Case |
|-------|----------|----------|
| **Garden** | Growth & cultivation | Incrementally build systems |
| **Budget** | Resource allocation | Optimize tokens, time, cost |
| **River** | Natural flow | Design workflows, pipelines |
| **Biopsychosocial** | Multi-dimensional | Analyze complex systems |
| **Alchemy** | Transformation | Learning, refactoring, self-improvement |

---

## 6. Multi-Agent Integration (Pluggable)

The framework is agnostic to the underlying agent system. Currently supported:

| Framework | Status | Use Case |
|-----------|--------|----------|
| **PydanticAI** ⭐ | Stub | Recommended: direct Claude integration |
| **CrewAI** | Stub | Team-based multi-agent orchestration |
| **Claude Agent SDK** | Stub | Official Anthropic agent SDK |
| **Claude-Flow** | Stub | Flow-based agent coordination |
| **PraisonAI** | Stub | Production-ready agent orchestration |

Adapters in `1_orchestration/agents/adapters/` implement the `BaseAgent` interface.

To use a specific framework:
1. Implement the adapter
2. Register in `agent_registry.py`
3. Update configuration

---

## 7. Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### Initialize Project Context

```bash
python src/main.py memory init
```

Creates `.context/` structure with:
- Constitution (`00_rules/project.md`)
- Session state (`01_state/`)
- Memory layers (`02_memory/`)
- Archive (`03_archive/`)

### Run Your First Workflow

#### Question Workflow
Ask the framework about itself:
```bash
/experts:framework:question "What are the 5 mental models?"
```

Executes `0_directives/40-workflows/question.md`:
1. Validate against codebase
2. Search for relevant information
3. Return answer with citations

#### Plan Workflow
Create a plan for a change:
```bash
/experts:websocket:plan "Add real-time notifications"
```

Executes `0_directives/40-workflows/plan.md`:
1. Analyze requirements
2. Design solution
3. Return step-by-step plan

#### Build Workflow
Implement the plan:
```bash
/experts:websocket:build < plan.md
```

Executes `0_directives/40-workflows/build.md`:
1. Implement changes
2. Run tests
3. Return change summary

#### Self-Improve Workflow
Learn from execution:
```bash
/experts:framework:self-improve
```

Executes `0_directives/40-workflows/self-improve.md`:
1. Extract facts from logs
2. Detect patterns
3. Update expertise.yaml

### Complete Cycle: Plan → Build → Improve

```bash
/experts:feature:plan_build_improve "Implement SSO"
```

Executes `0_directives/40-workflows/plan_build_improve.md`:
1. **Step 1**: Create plan → TaskOutput(plan.md)
2. **Step 2**: Implement changes → TaskOutput(build_report.md)
3. **Step 3**: Extract learning → TaskOutput(improvements.md)
4. **Step 4**: Update expertise → expertise.yaml updated

---

## 8. Expertise System

### What is Expertise?

A 4-pillar YAML structure describing what an agent knows and can do:

```yaml
# IDENTITY: Who is this?
name: database-expert
domain: postgresql

# CONTEXT: What mental models guide it?
mental_models: [garden, budget, river, ...]

# KNOWLEDGE: What does it know?
concepts:
  - name: Query Optimization
    confidence: 0.95
patterns:
  - name: N+1 Query Detection
    confidence: 0.85

# BEHAVIOR: What can it do?
workflows: [question, plan, build, self-improve]
```

### Expertise Validation

Expertise must be **validated against the codebase**:

1. Load `expertise.yaml`
2. Search codebase for matching patterns
3. Compare expertise claims vs. reality
4. Generate discrepancy report
5. Update expertise to match codebase

This is the `question` workflow.

### Self-Improving Expertise

After each cycle:
1. **FactExtractor** pulls triplets from session logs
2. **PatternRecognizer** detects repeated behaviors
3. **ReflectorAgent** analyzes and learns
4. **expertise.yaml** is updated with new knowledge

Over time, expertise becomes more accurate and comprehensive.

---

## 9. Best Practices

### ✅ DO

- Always validate expertise against codebase
- Use TaskOutput gates in multi-step workflows
- Document decisions in ADRs
- Store rules in `3_state/00_rules/` (immutable)
- Log session events for learning
- Review extracted facts and patterns

### ❌ DON'T

- Don't assume documentation is authoritative (code is)
- Don't skip TaskOutput gates (causes hallucination)
- Don't edit 00_rules without recording ADR
- Don't commit secrets to 3_state/
- Don't run workflows without exit criteria

---

## 10. Learning Resources

- **[CLAUDE.md](CLAUDE.md)** - Global AI operating context
- **[AGENTS.md](AGENTS.md)** - Agent system overview
- **[0_directives/README.md](0_directives/README.md)** - Directives system
- **[1_orchestration/README.md](1_orchestration/README.md)** - Orchestration layer
- **[3_state/README.md](3_state/README.md)** - Memory operations
- **[demos/](demos/)** - Working examples

---

## 11. Roadmap

### v0.1.0 (Current)
- [x] DOE architecture
- [x] Memory operations system
- [x] Multi-agent framework adapters (stubs)
- [x] Default expertise agents
- [x] Self-improvement pipeline

### v0.2.0 (Planned)
- [ ] Implement PydanticAI adapter fully
- [ ] Add BM25 semantic search for facts
- [ ] Enhanced pattern recognition
- [ ] Web UI for context visualization

### v0.3.0 (Future)
- [ ] CrewAI, Claude SDK full implementations
- [ ] LLM-powered fact extraction
- [ ] Distributed agent execution
- [ ] Marketplace for shared expertise

---

## 12. Support & Community

- File issues in GitHub
- Contribute expertise.yaml files for your domain
- Share learned patterns
- Propose framework improvements

---

**Version**: 0.1.0  
**Last Updated**: 2025-12-24  
**Status**: Production-Ready for Single-Agent; Multi-Agent Features in Beta
