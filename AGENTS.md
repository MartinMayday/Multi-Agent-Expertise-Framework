---
title: Multi-Agent Expertise Framework - File-Based Agentic Workflows OS
version: 1.0.0
author: MartinMayday
date: 2025-12-24
status: Production
classification: Internal Operations | Handoff to IDE/CLI AI Coders
framework: DOE + Elle + Expert-Framework
project: multi-agent-expertise-framework
output_expected: Complete file-based agentic orchestration system
execution_time: Reference + Demo deployment

contextual_snippets:
  - snippet: "DOE framework: Directives (The What) → Orchestration (The Who) → Execution (The How), with Elle context system providing state layer"
    keywords: [DOE, directives, orchestration, execution, state, Elle, context-memory]
    file: README.md
    tier: 1
  - snippet: "Progressive disclosure: L1 (index ~250 tokens) → L2 (metadata ~1000) → L3 (rich ~3000) → L4 (raw unlimited)"
    keywords: [progressive-disclosure, context-loading, token-optimization, tiers]
    file: 0_directives/AGENTS.md
    tier: 1

files:
  - name: 0_directives/AGENTS.md
    purpose: "Directive layer index - policies, goals, guardrails, workflows"
    use_when: "Need to understand WHAT the system should do"
    tier: 1
  - name: 1_orchestration/AGENTS.md
    purpose: "Orchestration layer index - AI decision-making, skills, agents"
    use_when: "Need to understand WHO decides and how"
    tier: 1
  - name: 2_executions/AGENTS.md
    purpose: "Execution layer index - tools, scripts, MCP servers"
    use_when: "Need to understand HOW things get done"
    tier: 1
  - name: 3_state/AGENTS.md
    purpose: "State layer index - sessions, memory, context, journal"
    use_when: "Need to understand persistent state and memory"
    tier: 1

key_concepts:
  - "DOE Pattern: Directives specify intent, Orchestration decides how to fulfill, Execution runs deterministic code"
  - "Elle Context System: 9-layer persistent context architecture"
  - "Progressive Disclosure: Load context in tiers to optimize token usage"
  - "KB-First Guardrails: Check knowledge base before research"
  - "Self-Annealing: System learns from corrections and updates expertise"
  - "TaskOutput Gates: Enforce sequential execution in multi-step workflows"

outcomes:
  - "Complete file-based agentic orchestration system"
  - "Ready for multi-agent framework integration"
  - "Production demos and reference implementations"
---
