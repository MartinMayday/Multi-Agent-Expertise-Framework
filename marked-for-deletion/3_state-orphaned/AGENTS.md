---
title: State Layer - The MEMORY
version: 1.0.0
contextual_snippets:
  - snippet: "State Layer: Persistent memory operations system. Handles session state, learned facts, and decision logs."
    keywords: [state, memory, session, journal, learning, self-annealing]
    file: README.md
    tier: 1

files:
  - name: 00_rules/project.md
    purpose: "Project mission and architecture constitution"
    tier: 1
  - name: 01_state/task_queue.json
    purpose: "DOE task state tracking"
    tier: 1
  - name: 02_memory/decisions.log.md
    purpose: "ADR-style decision log"
    tier: 2

key_concepts:
  - "Two-Tier Memory: Global (~/.expert-framework/) + Project (.context/)."
  - "Self-Annealing: System extracts facts and patterns from session logs."
  - "Audit Trail: Complete history of decisions and executions."
---
