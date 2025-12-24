---
name: Repository Preferences
description: How this repository likes to work — influences every interaction.
update_policy: When a new preference is stated, REPLACE the old one (don't accumulate contradictions). Add sections as needed. No permission required.
---

## Development Workflow

### Staging & Approval

<guide>How changes should be made</guide>

- **ALWAYS** write new/changed files to `review-approval/` or `staging/` first
- **NEVER** write directly to canonical locations (directives/, executions/, shared-knowledgebase/, agents/)
- **ALWAYS** create `review-approval/changeset.yaml` documenting changes
- **ALWAYS** run validation before promotion
- **ALWAYS** get approval before promoting

### Code Organization

<guide>How code should be structured</guide>

- **Python tools** go in `executions/tools/`
- **Workflows** go in `executions/workflows/`
- **Behavior contracts** go in `directives/`
- **Knowledge** goes in `shared-knowledgebase/`
- **Context memory** goes in `.context/`

## Communication Preferences

### Information Style

<guide>How agents should present information</guide>

- **Cite files** — Reference specific file paths when making claims
- **Be explicit** — No assumptions, no vague statements
- **Show evidence** — Trace all claims to documentation or execution results

### Decision Support

<guide>How agents should help with decisions</guide>

- **Show options** — Present 2-3 approaches with tradeoffs
- **Recommend** — But explain why
- **Flag risks** — Explicitly call out potential issues

### Tone

<guide>How agents should communicate</guide>

- **Professional but direct** — No fluff, get to the point
- **Factual** — Stick to what's known
- **Proactive** — Suggest improvements when gaps are found

## Working Style

### Task Approach

<guide>How tasks should be tackled</guide>

- **Plan first** — Understand requirements before implementing
- **Stage changes** — Never write directly to canonical locations
- **Validate** — Always run validation scripts
- **Document** — Update relevant docs when making changes

### Quality Standards

<guide>What quality means for this repo</guide>

- **No secrets** — Never commit tokens/keys
- **No assumptions** — All claims must trace to sources
- **Staging discipline** — Review before promotion
- **Context updates** — Keep `.context/` current

## Tools & Systems

### Development Tools

<guide>Preferred tools and systems</guide>

- **Python 3.12+** — For all execution tools
- **Markdown** — For all documentation
- **YAML** — For configuration (changeset.yaml, etc.)
- **Git** — For version control

### Validation Tools

<guide>Tools used for validation</guide>

- `scripts/validate_scaffold.py` — Structure validation
- `executions/tools/context_validator/` — Context validation (to be implemented)

## Decision-Making

### Risk Tolerance

<guide>How conservative vs. bold in recommendations</guide>

- **Conservative for canonical changes** — Staging + approval required
- **Bold for context updates** — Runtime-writable, autonomous updates

### Information Needs

<guide>Data-driven vs. intuition-trusting</guide>

- **Documentation-first** — Always check specs before acting
- **Evidence-based** — Trace all claims to sources
- **No assumptions** — If unsure, ask or research

### Speed vs. Thoroughness

<guide>Quick decisions vs. careful analysis</guide>

- **Thorough for canonical changes** — Validation + approval required
- **Quick for context updates** — Autonomous, immediate updates

## Boundaries

### Topics to Avoid

<guide>Anything agents shouldn't be involved in</guide>

- **Secrets management** — Never store or commit secrets
- **Runtime execution** — This is a file-based OS, not a runtime engine
- **Database systems** — File-based only

### Autonomy Level

<guide>How much agents should do independently vs. ask first</guide>

- **High autonomy for context updates** — Update `.context/` autonomously
- **Low autonomy for canonical changes** — Must stage and get approval
- **Medium autonomy for suggestions** — Propose improvements, but get approval before implementing

