# Directives

This directory contains behavior contracts that all agents must follow.

## Core Directives

### KB_GUARDRAILS.md
Mandatory KB-first execution protocol. Prevents agents from producing responses based on assumptions.

### HANDOFF_PROTOCOL.md
Formal state transfer between agents. Ensures work continuity and prevents state loss.

### PROGRESSIVE_LOADING.md
Context management rules. Prevents context window bloat by loading documentation in stages.

### FAILURE_HANDLING.md
Graceful failure handling. Makes failure a first-class outcome with explicit reporting.

## Enforcement

All directives are enforced by MetaGPT at the appropriate checkpoints:
- KB_GUARDRAILS: PRE_EXECUTION
- HANDOFF_PROTOCOL: POST_EXECUTION
- PROGRESSIVE_LOADING: CONTEXT_LOADING
- FAILURE_HANDLING: ERROR_DETECTION

## Usage

Agents must reference applicable directives in their system-instructions.md:

```markdown
## Instructions
- READ directives/KB_GUARDRAILS.md and follow strictly
- READ directives/HANDOFF_PROTOCOL.md before any agent transitions
- ...
```

## Templates

The `templates/` subdirectory contains workflow templates (plan.md, build.md, etc.) that are reference-only, not runtime directives.
