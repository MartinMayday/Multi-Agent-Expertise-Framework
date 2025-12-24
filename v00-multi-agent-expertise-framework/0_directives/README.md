# 0_directives - THE WHAT

This layer defines **what** the system does through policies, guardrails, and workflow contracts.

## Structure

```
0_directives/
├── 00-meta/          # Meta-documentation about the directive system
├── 10-global/        # Global policies and guardrails (ALWAYS/NEVER rules)
├── 20-roles/         # Agent persona contracts and responsibilities
├── 30-tools/         # Tool governance and error handling strategies
├── 40-workflows/     # Workflow templates (question, plan, build, improve)
├── 50-templates/     # Reusable directive templates
└── 90-output-contracts/  # Quality gates and handoff protocols
```

## Key Principles

1. **Directives are Constitutional** - They define immutable rules for agent behavior
2. **Guardrails First** - Check 10-global/ before executing any action
3. **Workflows are Contracts** - Each workflow defines expected inputs, steps, and outputs
4. **Output Quality Gates** - 90-output-contracts/ defines acceptance criteria

## Usage

All agents must:
1. Read `10-global/guardrails.md` at session start
2. Follow workflow templates from `40-workflows/` for structured tasks
3. Validate outputs against `90-output-contracts/` before completion
