---
name: Elle repo-context integration
overview: Integrate an Elle-inspired, in-repo `.context/` memory system into the agentic OS, and add IDE-agnostic entrypoints (`CLAUDE.md`, `GEMINI.md`, plus updates to `AGENTS.md`) so Cursor/Claude/Gemini users all load the same guardrails and repo context.
todos:
  - id: define-context-structure
    content: Design and stage Elle-inspired `.context/` repo-context skeleton (core files + conversations + update policy).
    status: completed
  - id: update-guardrails-contract
    content: Stage updates to `directives/STAGING_AND_APPROVAL.md`, add `directives/CONTEXT_MEMORY_SYSTEM.md`, and update `AGENTIC_WORKFLOW_CONTRACT.md` to include `.context/` semantics and permissions.
    status: completed
  - id: add-context-validator-tools
    content: Stage deterministic context validation tools under `executions/tools/context_validator/` and wire them into validation docs.
    status: completed
  - id: update-scaffold-and-validator
    content: Stage updates to `scripts/scaffold_os.py`, `scripts/validate_scaffold.py`, `src/agentic_os/paths.py`, `src/agentic_os/checks.py` to create/validate `.context/` and new directive.
    status: completed
  - id: add-ide-entrypoints
    content: Stage root `CLAUDE.md` + `GEMINI.md` and update `AGENTS.md` to reference `.context/` + entrypoints.
    status: completed
  - id: update-core-docs
    content: Stage doc updates (`FRAMEWORK.md`, `FRAMEWORK-CHECKLIST.md`, `README.md`, `.cursorignore`) to document `.context/` and prevent transcript context bloat.
    status: completed
---

# Integrate Elle-style `.context/` repo memory + multi-IDE entrypoints

## Goals

- Add an **Elle-inspired repo-context system** at **project root `.context/`** so AI/LLM + humans can persist: history, learnings, failures, evaluations, rollback notes, changelog links, and **full transcripts**.
- Make the framework **IDE/CLI agnostic** by generating consistent entrypoint docs for:
- Cursor (already: `.cursorrules`, `.cursor/rules/*`)
- Claude Code (`CLAUDE.md`)
- Gemini tooling (`GEMINI.md`)
- Existing in-repo catalog (`AGENTS.md`)
- Keep existing **staging policy** intact for code/contracts/tools, while allowing `.context/` to be **runtime-writable**.

## Constraints / non-negotiables

- **No verbatim copying** from the reference repo unless licensed/explicitly permitted. We will **recreate a tailored variant** using the reference structure as inspiration.
- **Staging-only for canonical code/docs**: all modifications go to `review-approval/` first, promoted only after validation + approval.
- **`.context/` is runtime-writable** (your choice): agents may write session logs and transcripts directly under `.context/` with strict structure + no-secrets rules.

## What we’ll implement

### 1) Add `.context/` as first-class OS component

Create a repo-local context system modeled after Elle’s core files, but tailored to “repo-context”:

- Add `.context/README.md` explaining purpose and what belongs here vs `sessions/`, `logs/`, `eval/`.
- Add `.context/context-update.md` (Elle-like “future self” test + update policies, adapted for repo use).
- Add `.context/core/` with:
- `identity.md` (repo identity + mission)
- `preferences.md` (repo-level preferences for agents/humans)
- `workflows.md` (repo SOPs, especially staging + validation)
- `relationships.md` (stakeholders/roles relevant to repo)
- `triggers.md` (release gates, recurring audits)
- `projects.md` (active epics/phases, links to `planning/`)
- `rules.md` (hard rules; includes “never write outside staging” + “no secrets”)
- `session.md` (current session focus; complements `planning/WORKSESSION_STATE.md`)
- `journal.md` (append-only notable decisions)
- Add `.context/conversations/` with:
- `README.md` describing naming convention and redaction rules
- transcript file template (frontmatter including `session_id`, `timestamp`, `participants`, `tools_used`, `redactions`)

### 2) Update guardrails to explicitly support `.context/`

- Update `directives/STAGING_AND_APPROVAL.md`:
- Add `.context/` to **allowed runtime write paths** (like `sessions/`/`logs/`), with strict rules:
    - transcripts append-only
    - no secrets
    - prefer summaries/links when possible, but you opted into full transcripts
- Update `AGENTIC_WORKFLOW_CONTRACT.md`:
- Add `.context/` to Root Structure and Permission Matrix
- Define `.context/` semantics (runtime-writable, audit trail, no-secrets)
- Add a new directive `directives/CONTEXT_MEMORY_SYSTEM.md`:
- Specifies **load order** (always read `.context/core/rules.md` first)
- Specifies **update triggers** (when to update `session.md`, `journal.md`, `rules.md`)
- Specifies **interaction with progressive loading** (don’t load full transcripts unless needed)
- Update `directives/README.md` to list new directive and checkpoint.

### 3) Add deterministic validation tooling for `.context/`

Create an execution tool suite to keep `.context/` consistent and safe:

- Add `executions/tools/context_validator/`:
- `validate_context_tree.py` (required files/dirs exist)
- `validate_transcript_metadata.py` (frontmatter present, no forbidden patterns like obvious API keys)
- `README.md` usage
- Update `scripts/validate_scaffold.py` + `src/agentic_os/checks.py`:
- Include `.context/` checks
- Include new directive existence checks

### 4) Ensure scaffold generator creates `.context/` skeleton

- Update `scripts/scaffold_os.py` and `src/agentic_os/paths.py`:
- Add `.context` as canonical path
- Scaffold the `.context/` skeleton on fresh setup

### 5) Multi-IDE entrypoints: `CLAUDE.md` + `GEMINI.md` + update `AGENTS.md`

- Add root `CLAUDE.md`:
- Minimal entrypoint instructing Claude Code to read:
    - `AGENTIC_WORKFLOW_CONTRACT.md`
    - directives (KB-first, staging, progressive loading)
    - `.context/core/rules.md` and `.context/core/session.md`
- Emphasize runtime-writable `.context/` and staging-only for canonical changes
- Add root `GEMINI.md`:
- Same structure and constraints; keeps behavior consistent for Gemini-based IDE/CLI flows
- Update `AGENTS.md`:
- Add a short “Repo Context System” section pointing to `.context/`
- Add an “IDE Entrypoints” section listing `.cursorrules`, `CLAUDE.md`, `GEMINI.md`

### 6) Update core documentation

- Update `FRAMEWORK.md`:
- Replace vague “Elle-inspired” mentions with explicit `.context/` architecture, load/update policies, and how it differs from `shared-knowledgebase/`.
- Update `FRAMEWORK-CHECKLIST.md`:
- Add `.context/` presence checks
- Add “context validator tool” checks
- Update `README.md`:
- Add “Repo Context System (.context)” section

### 7) Cursor context-bloat control

- Update `.cursorignore`:
- Exclude `.context/conversations/` by default (transcripts are huge)
- Keep `.context/core/` included so agents always load rules/session quickly
- Document how to load a specific transcript on demand when needed

## Staging / Promotion workflow

All canonical file changes are staged first:

- Create everything under `review-approval/` as the proposed canonical tree
- Fill out `review-approval/changeset.yaml` listing source→target paths
- Run:
- `python scripts/validate_scaffold.py --project-root . -v`
- `python executions/tools/context_validator/validate_context_tree.py` (once added)
- Produce approval checklist; promote only after your approval

## Files we will add/update (high signal)

- Add: `.context/**` (core + conversations)
- Add: `CLAUDE.md`, `GEMINI.md`
- Add: `directives/CONTEXT_MEMORY_SYSTEM.md`
- Update: `directives/STAGING_AND_APPROVAL.md`, `directives/README.md`
- Update: `AGENTIC_WORKFLOW_CONTRACT.md`, `FRAMEWORK.md`, `FRAMEWORK-CHECKLIST.md`, `AGENTS.md`, `README.md`
- Add: `executions/tools/context_validator/**`
- Update: `scripts/scaffold_os.py`, `scripts/validate_scaffold.py`, `src/agentic_os/paths.py`, `src/agentic_os/checks.py`
- Update: `.cursorignore` (ignore `.context/conversations/`)

## Acceptance criteria

- `.context/` exists with required core files and transcript conventions.
- Contract + directives clearly define `.context/` behavior and write permissions.
- Validation scripts catch missing/invalid `.context/` structure.
- `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, and `AGENTS.md` all point to the same guardrails and `.context/`.