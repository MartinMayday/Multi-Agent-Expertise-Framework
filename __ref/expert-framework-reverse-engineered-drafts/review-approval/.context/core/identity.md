---
name: Repository Identity
description: Who this repository is — stable facts that shape how agents should understand and serve it.
update_policy: Update autonomously when new information is shared. Add sections as needed. No permission required.
---

## Repository Name

**Expert Framework Agentic OS** — A file-based agentic workflow operating system

## Core Purpose

This repository implements a **file-based agentic workflow OS** where AI/LLM acts as orchestrator over deterministic Python tools. The system is IDE/CLI agnostic and enforces documentation-first, hallucination-resistant agent behaviors.

## Mission

Enable autonomous AI/LLM orchestration with:
- **KB-first execution** — Always check knowledge base before responding
- **Filesystem-as-API** — Explicit contracts for all paths and permissions
- **Staging-only writes** — All canonical changes go through review-approval
- **Progressive loading** — Efficient context management
- **Handoff discipline** — Formal state transfer between agents
- **Repo-context memory** — Never start from scratch, always build upon earlier work

## Scope

<guide>What this repo covers and what it doesn't</guide>

**In Scope:**
- File-based agentic workflow orchestration
- Multi-agent coordination (MetaGPT + 7 specialized agents)
- Knowledge base management
- Execution tool framework
- Context memory system
- Multi-IDE support (Cursor, Claude Code, Gemini)

**Out of Scope:**
- Runtime execution engines (agents use external LLM APIs)
- Database systems (file-based only)
- Web interfaces (CLI/IDE focused)

## Architecture Principles

<guide>Core architectural decisions that guide all development</guide>

1. **No assumptions** — All responses trace to documentation, KB, or execution results
2. **Deterministic tools** — Complex logic in Python, not LLM reasoning
3. **Explicit contracts** — Filesystem-as-API with clear permissions
4. **Staging-first** — All changes reviewed before promotion
5. **Context persistence** — Repo memory enables continuous improvement

## Technology Stack

<guide>Key technologies and tools used</guide>

- **Language**: Python 3.12+
- **Orchestration**: File-based (no runtime dependencies)
- **LLM Support**: Multi-provider (Anthropic, OpenAI, Gemini, etc.)
- **IDE Support**: Cursor, Claude Code, Gemini tooling
- **Validation**: Python scripts (`validate_scaffold.py`)

## Current State

<guide>Where the repo is in its lifecycle</guide>

**Status**: In active development
**Current Phase**: Phase 2 complete (Cursor runtime + staging), Phase 3 in progress (Agent instructions)
**Maturity**: Alpha/early beta

## Goals & Aspirations

### Near-Term (This Quarter)

<guide>Goals for the next 3 months</guide>

- Complete all 7 agent system instructions
- Implement execution tools
- Populate knowledge base
- Establish testing framework

### Long-Term (6+ Months)

<guide>Bigger vision for the repository</guide>

- Production-ready agentic OS
- Comprehensive evaluation framework
- Self-improving agent behaviors
- Community adoption

## Current Challenges

<guide>Obstacles, frustrations, pain points</guide>

- Agent instructions need encoding of all directives
- Execution tools need implementation
- Knowledge base needs population
- Testing framework needs creation

## Values & Principles

<guide>What matters to this repository — guides decision-making</guide>

- **Documentation-first** — Specs before implementation
- **No secrets** — Never commit tokens/keys
- **Staging discipline** — Review before promotion
- **Context accumulation** — Learn from every session
- **Transparency** — All decisions traceable

## Communication Style

<guide>How agents should communicate about this repo</guide>

- Direct, factual, cite files
- No assumptions, no hallucinations
- Clear about what's missing or blocked
- Proactive about suggesting improvements

