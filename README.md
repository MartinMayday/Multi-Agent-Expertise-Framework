# Multi-Agent Expertise Framework

> File-based agentic OS combining DOE (Directives→Orchestration→Execution), Elle Context, and self-improving expertise.

## What Is It?

**[→ Read FRAMEWORK.md for complete architecture and concepts](FRAMEWORK.md)**

A production-ready operating system for autonomous AI agents that:
- Separates concerns into **Directives** (policies), **Orchestration** (agents), **Execution** (tools), and **Memory** (learning)
- Validates expertise against codebase (no hallucination)
- Learns and improves automatically (self-annealing)
- Supports pluggable multi-agent frameworks (PydanticAI, CrewAI, Claude SDK, PraisonAI, Claude-Flow)
- Uses progressive disclosure to optimize token usage

## Architecture

```
┌─ 0_directives/          ─ THE WHAT ─────┐
│  Policies, guardrails,                   │
│  workflows, templates                    │
├─ 1_orchestration/       ─ THE WHO ──────┤
│  Agents, mental models,                  │
│  skills, expertise                       │
├─ 2_executions/          ─ THE HOW ──────┤
│  Tools, utilities, workflows             │
├─ 3_state/               ─ MEMORY ───────┤
│  Rules, state, facts,                    │
│  patterns, sessions                      │
└─ src/                   ─ IMPLEMENTATION─┘
```

## Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Initialize Project Context
```bash
python src/main.py memory init
```

Creates `.context/` with constitution, session state, memory layers, and archives.

### 3. Ask a Question
```bash
/experts:framework:question "What are the 5 mental models?"
```

### 4. Create a Plan
```bash
/experts:feature:plan "Implement real-time notifications"
```

### 5. Complete Workflow (Plan → Build → Learn)
```bash
/experts:feature:plan_build_improve "Add user authentication"
```

## Key Features

| Feature | Purpose |
|---------|---------|
| **DOE Architecture** | Clear separation of What/Who/How |
| **Expertise Validation** | Codebase is authoritative (no hallucination) |
| **Self-Improvement** | Learns from sessions via facts and patterns |
| **TaskOutput Gates** | Enforces sequential execution, prevents context loss |
| **Progressive Disclosure** | L1-L4 context loading optimizes tokens |
| **Multi-Agent Ready** | Pluggable adapters for PydanticAI, CrewAI, etc. |
| **Two-Tier Memory** | Global (~/.expert-framework/) + Project (3_state/) |
| **Mental Models** | 5 cognitive frameworks (garden, budget, river, biopsychosocial, alchemy) |

## Files to Read

1. **[FRAMEWORK.md](FRAMEWORK.md)** (START HERE)
   - What it is, key concepts, architecture, invocation patterns
   - Getting started guide with examples
   - Expertise system explanation
   
2. **[CLAUDE.md](CLAUDE.md)**
   - Global AI operating context
   - Authority hierarchy and sequential execution rules
   
3. **[AGENTS.md](AGENTS.md)**
   - Agent system overview
   - Layer indices and structure
   
4. **[0_directives/](0_directives/)**
   - Policies, guardrails, workflow definitions
   
5. **[demos/](demos/)**
   - Working examples of each workflow

## Success Criteria (v0.1.0)

- [x] DOE structure with proper numbered directories
- [x] Memory Operations System (Phase 1-5 complete)
- [x] Multi-agent framework interfaces and adapters
- [x] Default reference expertise agents (research, code, devops)
- [x] FRAMEWORK.md blueprint
- [x] Clean repository structure (no duplicates or clutter)
- [x] Self-improvement pipeline ready

## Roadmap

**v0.2.0**: Full PydanticAI adapter, enhanced semantic search  
**v0.3.0**: CrewAI, Claude SDK integrations, distributed execution  
**v1.0.0**: Production hardening, marketplace for shared expertise

## License

MIT

---

**Status**: Production-Ready for Single-Agent | Multi-Agent Features in Beta  
**Version**: 0.1.0  
**Last Updated**: 2025-12-24
