---
name: Staging + Cursor runtime
overview: Add strict staging/approval guardrails (review-approval/ + staging/) and Cursor IDE runtime assets (.cursorrules entrypoint, project rules, slash commands, cursorignore), plus a resumable roadmap/status file so future sessions can continue deterministically.
todos:
  - id: staging-folders
    content: Add `review-approval/` + `staging/` folders with README and a standard changeset template for staged work.
    status: completed
  - id: staging-guardrails
    content: Implement staging-only write policy in `.cursorrules`, `directives/STAGING_AND_APPROVAL.md`, and update `AGENTIC_WORKFLOW_CONTRACT.md` to include staging paths and forbidden direct writes.
    status: completed
  - id: cursor-project-rules
    content: Create `.cursor/rules/project_rules.mdc` (alwaysApply) encoding KB-first/progressive loading/handoff + staging-only write + root hygiene.
    status: completed
  - id: cursor-commands-full
    content: Populate `.cursor/commands/` with the full command set plus staging/promotion commands, aligned to existing scripts/templates.
    status: completed
  - id: cursorignore
    content: Create `.cursorignore` to exclude provenance/noise directories and secrets while keeping sessions selectively loadable.
    status: completed
  - id: roadmap-and-state
    content: Create `planning/ROADMAP.md`, `planning/WORKSESSION_STATE.md`, and `planning/REVIEW_APPROVAL_QUEUE.md` so future sessions can resume deterministically.
    status: completed
  - id: root-hygiene
    content: Move `ROOT_CLEANUP_COMPLETE.md` out of root into `marked-for-deletion/` (dedupe).
    status: completed
---

# Staging/approval guardrails + Cursor

runtime assets

## Objectives

- Enforce a **hard guardrail**: AI/LLM writes changes into **staging only** (using `review-approval/` and `staging/`), and can only promote to canonical locations after **validation + approval**.
- Add **Cursor IDE runtime files** so future sessions start with consistent constraints and reusable slash commands.
- Produce a **resumable roadmap/status** artifact in `planning/` so you can say “resume” and the AI continues phase→tasks→subtasks.

## Current repo facts (verified)

- `.cursorrules` exists.
- `.cursor/commands/` exists but is empty.
- `.cursor/rules/` exists but is empty; `project_rules.mdc` is missing.
- `.cursorignore` is missing.
- Root currently contains a non-essential file `ROOT_CLEANUP_COMPLETE.md` (duplicate also exists in `marked-for-deletion/`).
- `planning/` exists and is empty.

## Implementation plan

### 1) Add staging areas (repo root)

- Create `review-approval/` and `staging/` with:
- `README.md` explaining purpose and promotion gate.
- A standard **change bundle** pattern:
    - `review-approval/changeset.yaml` (what to change, why, target paths)
    - `review-approval/patches/` (optional diffs)
    - `staging/out/` (tool outputs, generated files, logs)

### 2) Encode staging guardrails into repo rules/contracts

- Update **`.cursorrules`** to state:
- Default write location is **staging only**.
- Direct edits outside staging require explicit user permission.
- Add a directive: `directives/STAGING_AND_APPROVAL.md` defining:
- Allowed write paths by default.
- Required validation steps before promotion.
- Required “approval checklist” output.
- Update `AGENTIC_WORKFLOW_CONTRACT.md` to include `review-approval/` + `staging/` as first-class OS paths and forbidden direct-write behavior.

### 3) Add Cursor project rules

- Create `.cursor/rules/project_rules.mdc` (alwaysApply, globs **/*) with:
- KB-first enforcement hooks (references `directives/KB_GUARDRAILS.md`).
- Progressive loading rules (references `directives/PROGRESSIVE_LOADING.md`).
- Handoff contract requirements (references `directives/HANDOFF_PROTOCOL.md`).
- **Staging-only write** policy + promotion gate.
- Root hygiene rules.

### 4) Add Cursor slash commands (full set)

- Populate `.cursor/commands/` with commands from the earlier plan plus staging-specific commands:
- `/validate-scaffold`
- `/scaffold-os`
- `/kb-first-answer`
- `/create-kb-snippet`
- `/handoff`
- `/create-execution-tool`
- `/create-execution-workflow`
- `/failure-triage`
- `/eval-maturity`
- `/plan-build-self-improve`
- **New**: `/stage-changes` (create `changeset.yaml` + stage outputs)
- **New**: `/promote-staged-changes` (run promotion tool, require validation + approval)

### 5) Add `.cursorignore`

- Create `.cursorignore` excluding:
- `original-repo/`, `marked-for-deletion/`
- `**/__pycache__/`, `*.log`
- `.env`, `.env.*`
- (Keep `sessions/` included; include rule guidance to load selectively.)

### 6) Add resumable roadmap/status artifacts

- Create in `planning/`:
- `planning/ROADMAP.md` (phases → tasks → subtasks)
- `planning/WORKSESSION_STATE.md` (what’s done, what’s next, what’s blocked)
- `planning/REVIEW_APPROVAL_QUEUE.md` (what’s staged and pending approval)

### 7) Root hygiene cleanup

- Move `ROOT_CLEANUP_COMPLETE.md` from root into `marked-for-deletion/` (keep only one copy).

## Validation / gates

- `python scripts/validate_scaffold.py --project-root . -v`
- Promotion gate: only allow promoting staged changes after validation passes and you approve the checklist.

## Files to add/update (by location)

- Add: `review-approval/README.md`, `review-approval/changeset.yaml` (template), `review-approval/patches/`
- Add: `staging/README.md`, `staging/out/`
- Add: `directives/STAGING_AND_APPROVAL.md`, update `directives/README.md`
- Update: `.cursorrules`, `AGENTIC_WORKFLOW_CONTRACT.md`
- Add: `.cursor/rules/project_rules.mdc`
- Add: `.cursor/commands/*.md` (full set + staging commands)