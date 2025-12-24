---
title: Multi-Agent Expertise Framework v0.1.0
status: Launch-Ready
framework: Strict DOE + Extended Memory OS
progressive_disclosure: L1-L4 implemented via context_engine.py

contextual_snippets:
  - snippet: "DOE: Directives (WHAT) → Orchestration (WHO) → Execution (HOW). State layer handles persistent memory."
    keywords: [DOE, orchestration, execution, state, memory]
    file: README.md
    tier: 1

files:
  - name: 0_directives/10-global/guardrails.md
    purpose: "✅ ALWAYS / ❌ NEVER hard constraints"
    tier: 1
  - name: 1_orchestration/context_engine.py
    purpose: "L1-L4 context management logic"
    tier: 1
  - name: 3_state/01_state/task_queue.json
    purpose: "Operational task state"
    tier: 1

key_concepts:
  - "TaskOutput Gates: Enforced sequential dependency management."
  - "Two-Tier Memory: Unified resolution across Global and Project scopes."
  - "Self-Annealing: Automated fact and pattern extraction."
---
