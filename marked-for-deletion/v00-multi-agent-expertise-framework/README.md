# Multi-Agent Expertise Framework

> File-based agentic workflows OS combining DOE, Elle Context, and 7-agent pipeline.

## Overview

The Multi-Agent Expertise Framework is a production-ready, sophisticated orchestration system designed for autonomous AI/LLM workers. It separates concerns into Directives (The What), Orchestration (The Who), and Execution (The How), supported by a robust Memory Operations System.

## Architecture

- **0_directives/**: The "WHAT". Goals, policies, guardrails, and workflow definitions.
- **1_orchestration/**: The "WHO". AI decision-making, specialized agents, mental models, and skills.
- **2_executions/**: The "HOW". Deterministic Python tools, workflows, and utilities.
- **3_state/**: The "MEMORY". Persistent session state, learned facts, and decision logs.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Global Context**:
   Follow instructions in `docs/GLOBAL_CONTEXT_SETUP.md` to create `~/.claude/`.

3. **Initialize Project**:
   ```bash
   python src/main.py memory init
   ```

4. **Run a Workflow**:
   ```bash
   /experts:websocket:plan_build_improve "Implement session counter"
   ```

## Key Principles

- **Expertise Validation**: The codebase is the source of truth. Expertise files must be validated against actual implementation.
- **Sequential Chaining**: Complex tasks are executed in sequence using TaskOutput gates.
- **Rules-First**: Hard constraints (NEVER/ALWAYS) are checked before any decision-making.
- **Progressive Disclosure**: Context is loaded in layers (L1-L4) to optimize token usage.

## License

MIT
