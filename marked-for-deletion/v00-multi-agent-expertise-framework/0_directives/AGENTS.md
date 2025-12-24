# Directives Layer Index

**Layer**: 0_directives (THE WHAT)
**Purpose**: Define policies, guardrails, and workflow contracts

## Subdirectories

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `00-meta/` | Meta-documentation | How the directive system works |
| `10-global/` | Global policies | guardrails.md, policies.md |
| `20-roles/` | Agent personas | Role definitions and contracts |
| `30-tools/` | Tool governance | error-handling-strategy.md |
| `40-workflows/` | Workflow templates | question.md, plan.md, build.md |
| `50-templates/` | Reusable templates | expertise.yaml.example |
| `90-output-contracts/` | Quality gates | Output validation rules |

## Loading Priority

1. **L1 (Always)**: 10-global/guardrails.md
2. **L2 (Role)**: 20-roles/[current-role].md
3. **L3 (Task)**: 40-workflows/[workflow].md
4. **L4 (Full)**: All relevant directives for complex tasks
