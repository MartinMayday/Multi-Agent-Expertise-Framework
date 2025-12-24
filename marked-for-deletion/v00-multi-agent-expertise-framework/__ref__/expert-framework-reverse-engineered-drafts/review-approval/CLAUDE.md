# Claude Code Entrypoint

This file provides entrypoint instructions for Claude Code when working with this repository.

## System Overview

This repository implements a **file-based agentic workflow OS** where AI acts as orchestrator over deterministic Python tools. The system is IDE/CLI agnostic and enforces documentation-first, hallucination-resistant agent behaviors.

## Required Reading (In Order)

Before taking any action, read these files in this order:

1. **`AGENTIC_WORKFLOW_CONTRACT.md`** - Filesystem-as-API contract, permissions, ownership
2. **`directives/KB_GUARDRAILS.md`** - KB-first execution protocol (MANDATORY)
3. **`directives/STAGING_AND_APPROVAL.md`** - Staging-only write policy (MANDATORY)
4. **`directives/CONTEXT_MEMORY_SYSTEM.md`** - Context loading/update protocol (MANDATORY)
5. **`.context/core/rules.md`** - Hard rules (ALWAYS check first before any action)
6. **`.context/core/session.md`** - Current session focus

## Core Principles

1. **No assumptions** - All responses must trace to documentation, KB, or execution results
2. **KB-first execution** - Check `shared-knowledgebase/manifest.md` before answering; declare KB_STATUS
3. **Staging-only writes** - ALL new/changed files MUST be written to `review-approval/` or `staging/` first
4. **Context memory** - Always check `.context/core/rules.md` first; update `.context/` autonomously
5. **No secrets** - Never commit tokens/keys; use `.env` files (excluded from context)
6. **Cite files** - Reference specific file paths when making claims

## Write Policy

**Runtime-Writable (Direct Writes Allowed):**
- `.context/` - Repo-context memory (with strict rules: no secrets, append-only transcripts)
- `sessions/` - Agent execution history
- `logs/` - Execution logs

**Staging-Required (Must Go Through review-approval/):**
- `directives/` - Behavior contracts
- `executions/` - Python tools and workflows
- `shared-knowledgebase/` - Cross-agent knowledge
- `agents/` - Agent definitions
- Root documentation files

## Context Loading Order

1. **Always first**: `.context/core/rules.md` (check before ANY action)
2. **For substantive tasks**: `.context/core/identity.md`, `.context/core/preferences.md`, `.context/core/workflows.md`, `.context/core/session.md`
3. **On-demand only**: `.context/core/projects.md`, `.context/core/relationships.md`, `.context/core/triggers.md`, `.context/core/journal.md` (selective), `.context/conversations/[specific-session].md`

**Never load:**
- All transcripts from `.context/conversations/` upfront (context bloat)
- Entire `journal.md` (selective entries only)

## Agent Catalog

See `AGENTS.md` for the complete agent catalog and capabilities.

## Quick Reference

- **Staging changes**: Write to `review-approval/` or `staging/`, create `changeset.yaml`
- **Promoting changes**: Use `/promote-staged-changes` after validation + approval
- **Updating context**: Update `.context/core/session.md` during session, append to `journal.md` after notable sessions
- **Creating transcripts**: After session, create in `.context/conversations/` with redactions for secrets

## See Also

- `.cursorrules` - Cursor IDE entrypoint (similar principles)
- `GEMINI.md` - Gemini tooling entrypoint (similar principles)
- `AGENTS.md` - Agent catalog
- `FRAMEWORK.md` - Complete system architecture
- `FRAMEWORK-CHECKLIST.md` - Deployment validation criteria

