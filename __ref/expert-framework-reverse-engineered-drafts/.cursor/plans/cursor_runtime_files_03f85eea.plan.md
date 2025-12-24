---
name: Cursor runtime files
overview: "Add production-grade Cursor IDE runtime guidance for this agentic OS: a minimal `.cursorrules` entrypoint, detailed `.cursor/rules/project_rules.mdc`, and a full set of `.cursor/commands/*.md` slash commands aligned with the repo’s directives/executions contracts."
todos:
  - id: add-cursorrules-entrypoint
    content: Create minimal root `.cursorrules` that points to authoritative repo specs and defers detailed policy to `.cursor/rules/project_rules.mdc`.
    status: completed
  - id: add-project-rules-mdc
    content: Add `.cursor/rules/project_rules.mdc` with YAML frontmatter and repo-specific non-negotiables (KB-first, progressive loading, handoff protocol, filesystem-as-API, root hygiene).
    status: in_progress
  - id: add-cursor-commands
    content: Create `.cursor/commands/` with the full slash-command set for scaffold/validate, KB operations, handoff, tool/workflow scaffolding, failure triage, and plan-build-self-improve loop.
    status: pending
  - id: add-cursorignore
    content: Add `.cursorignore` excluding `original-repo/`, `marked-for-deletion/`, caches, logs, and env files (keep sessions included by default).
    status: pending
  - id: update-readme-cursor-section
    content: Update `README.md` to document Cursor runtime files locations and intended usage.
    status: pending
---

# Cursor IDE runtime files (rules + slash commands)

## Goals
- Ensure Cursor has **authoritative, production-grade** project guidance without relying on ad-hoc conversation context.
- Provide **reusable slash commands** that operationalize this repo’s contracts: KB-first, filesystem-as-API, directives vs executions separation, and handoff discipline.
- Keep the **root clean** (only essential project files) while still supporting Cursor runtime.

## What we’ll add

### 1) Cursor entrypoint rules (root)
- Create **`.cursorrules`** as a *short* entrypoint (per your choice to use both):
  - Points Cursor to the authoritative specs: `AGENTIC_WORKFLOW_CONTRACT.md`, `FRAMEWORK.md`, `FRAMEWORK-CHECKLIST.md`, `AGENTS.md`.
  - States the non-negotiables: **no assumptions**, **KB-first**, **cite files**, **no secrets**, **follow filesystem-as-API**.
  - Delegates all detail to `.cursor/rules/project_rules.mdc`.

Notes:
- Cursor’s current guidance favors `.cursor/rules/*.mdc` over `.cursorrules`, but you selected both; we’ll keep `.cursorrules` minimal to avoid rule duplication.

### 2) Detailed project rules
- Create **`.cursor/rules/project_rules.mdc`** (Markdown + YAML frontmatter) with:
  - `alwaysApply: true`
  - `globs: "**/*"`
  - Sections tuned to this repo:
    - **Authority order** (what files override what)
    - **KB-first gate** (aligned to `directives/KB_GUARDRAILS.md`)
    - **Progressive loading** (aligned to `directives/PROGRESSIVE_LOADING.md`)
    - **Handoff protocol** (aligned to `directives/HANDOFF_PROTOCOL.md`)
    - **Filesystem-as-API** (where new artifacts must go: `directives/`, `executions/`, `shared-knowledgebase/`, etc.)
    - **Root hygiene** (root is reserved for essential runtime docs only)
    - **Operational commands** (callouts to `.cursor/commands/*`)

### 3) Slash commands (full set)
- Create **`.cursor/commands/`** with Markdown prompt files (Cursor loads these as slash commands).

Proposed command set (file names are the command names):
- **`.cursor/commands/validate-scaffold.md`**: Run `python scripts/validate_scaffold.py --project-root . -v`, interpret failures, and produce a fix plan.
- **`.cursor/commands/scaffold-os.md`**: Run `python scripts/scaffold_os.py --apply --force`, explain when to use `--dry-run`, and how to review generated diffs.
- **`.cursor/commands/kb-first-answer.md`**: Enforce KB gate: read `shared-knowledgebase/manifest.md` + agent KB manifests; output `KB_STATUS` + “blocked if insufficient.”
- **`.cursor/commands/create-kb-snippet.md`**: Generate a KB snippet using the repo’s snippet format (and require sources/traceability).
- **`.cursor/commands/handoff.md`**: Emit the handoff JSON contract exactly as defined in `directives/HANDOFF_PROTOCOL.md`.
- **`.cursor/commands/create-execution-tool.md`**: Scaffold a new deterministic Python tool in `executions/tools/` + minimal docs and a validation hook (no invented behavior; require spec inputs).
- **`.cursor/commands/create-execution-workflow.md`**: Scaffold a workflow in `executions/workflows/` plus any required directive stub in `directives/`.
- **`.cursor/commands/failure-triage.md`**: Standard failure response: reproduce, isolate, propose minimal fix, add validation steps, and record next actions.
- **`.cursor/commands/eval-maturity.md`**: If an eval runner exists, run it; otherwise create a spec + request for `executions/eval/` tooling (no pretending it exists).
- **`.cursor/commands/plan-build-self-improve.md`**: Drive the “plan → build → self-improve” loop using existing templates in `directives/templates/`.

### 4) Context exclusion (production-relevant)
- Create **`.cursorignore`** at repo root to prevent Cursor from loading non-production noise by default:
  - Always ignore: `original-repo/`, `marked-for-deletion/`, `**/__pycache__/`, `*.log`, `.env`, `.env.*`
  - Keep `sessions/` *included* by default (it’s part of the OS), but add guidance in rules to only open relevant session artifacts.

## Files we will touch/add
- Add: [`.cursorrules`](/Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/.cursorrules)
- Add: [`.cursor/rules/project_rules.mdc`](/Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/.cursor/rules/project_rules.mdc)
- Add: [`.cursor/commands/*`](/Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/.cursor/commands/)
- Add: [`.cursorignore`](/Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/.cursorignore)
- Update (small): [`README.md`](/Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/README.md) to mention Cursor runtime files and where they live.

## Validation
- Confirm the repo still validates:
  - Run `python scripts/validate_scaffold.py --project-root . -v`
- Confirm Cursor runtime picks up:
  - `.cursor/rules/project_rules.mdc`
  - `.cursor/commands/*`
  - `.cursorrules`

(We can’t fully validate Cursor UI behavior in this environment, but we’ll keep the structure aligned to Cursor’s documented conventions.)