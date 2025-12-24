---
name: Rules
description: These are explicit rules learned from past mistakes or corrections. **ALWAYS check these before taking action.**
update_policy:
- ADD rules when user corrects behavior or expresses frustration about an action (no permission needed)
- Only REMOVE rules when user explicitly rescinds them (no permission needed)
- Add new sections as needed (no permission needed)
rule_format:
- ❌ NEVER [action] [context if needed] - [reason/origin if helpful]
- ✅ ALWAYS [action] [context if needed]
---

<guide>
Rules are learned from corrections. Add new sections as categories emerge.
Use the format from the frontmatter:
- ❌ NEVER [action] [context] - [reason]
- ✅ ALWAYS [action] [context]
</guide>

## Staging & Approval

- ❌ NEVER write to canonical locations (directives/, executions/, shared-knowledgebase/, agents/) without staging first
- ✅ ALWAYS write new/changed files to review-approval/ or staging/ first
- ✅ ALWAYS create changeset.yaml documenting changes
- ✅ ALWAYS run validation before promotion
- ✅ ALWAYS get approval before promoting staged changes
- ❌ NEVER skip validation steps
- ❌ NEVER promote without approval

## Secrets & Security

- ❌ NEVER commit tokens, keys, passwords, or credentials
- ❌ NEVER hardcode API keys in code
- ❌ NEVER expose secrets in logs, outputs, or transcripts
- ✅ ALWAYS use .env files (excluded from context via .cursorignore)
- ✅ ALWAYS redact secrets in transcripts with [REDACTED: reason] markers

## Documentation & Evidence

- ❌ NEVER make assumptions — all responses must trace to documentation, KB, or execution results
- ✅ ALWAYS cite specific file paths when making claims
- ✅ ALWAYS check shared-knowledgebase/manifest.md before answering
- ✅ ALWAYS declare KB_STATUS (sufficient|partial|insufficient)
- ❌ NEVER claim "works" without validation steps

## Context & Memory

- ✅ ALWAYS check .context/core/rules.md before taking any action
- ✅ ALWAYS update .context/core/session.md with current focus
- ✅ ALWAYS add rules to .context/core/rules.md when corrections are made
- ❌ NEVER modify conversation transcripts after creation (append-only)
- ✅ ALWAYS create transcripts after each session in .context/conversations/

## Agent Behavior

- ❌ NEVER skip KB-first checks
- ❌ NEVER skip handoff protocol
- ❌ NEVER load entire knowledgebase into context (use progressive loading)
- ✅ ALWAYS emit handoff contract when transferring work
- ✅ ALWAYS follow directives (KB_GUARDRAILS, HANDOFF_PROTOCOL, PROGRESSIVE_LOADING, STAGING_AND_APPROVAL, CONTEXT_MEMORY_SYSTEM)

## Root Hygiene

- ❌ NEVER add temporary documentation to root
- ❌ NEVER add status files to root
- ❌ NEVER add conversation artifacts to root
- ✅ ALWAYS keep root clean — only essential runtime docs (FRAMEWORK.md, AGENTIC_WORKFLOW_CONTRACT.md, AGENTS.md, FRAMEWORK-CHECKLIST.md, README.md)

