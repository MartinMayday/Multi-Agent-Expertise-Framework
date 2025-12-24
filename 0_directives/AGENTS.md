---
title: Directives Layer - The WHAT
version: 1.0.0
contextual_snippets:
  - snippet: "Directives Layer: Specifies intent, workflows, triggers, and constraints. Defines WHAT the system should do."
    keywords: [directives, intent, constraints, workflows, policies]
    file: README.md
    tier: 1

files:
  - name: core/KB_GUARDRAILS.md
    purpose: "Mandatory KB-first execution protocol"
    tier: 1
  - name: workflows/plan_build_improve.md
    purpose: "Primary 3-phase orchestration workflow"
    tier: 1
  - name: workflows/question.md
    purpose: "Q&A mode with expertise validation"
    tier: 1
  - name: templates/expertise.yaml.example
    purpose: "4-pillar knowledge structure template"
    tier: 2

key_concepts:
  - "DOE Pattern: Directives layer is the authoritative source of truth for behavior."
  - "Validation: Documentation is validated against implementation in every workflow."
  - "Sequential Execution: Steps are gated by TaskOutput retrieval."
---
