# Repo Context System (.context/)

This directory contains the **repository's persistent memory** — a context system that enables AI/LLM and humans to build upon earlier work, never starting from scratch.

## Purpose

The `.context/` system stores:
- **History**: Full conversation transcripts, session logs, decision records
- **Learnings**: Patterns, failures, successful approaches
- **Evaluations**: Maturity scores, reliability metrics, improvement notes
- **Rollback notes**: What changed, why, and how to revert if needed
- **Repo changelog**: Links to significant changes and their rationale
- **Conversation logs**: Complete transcripts of AI/LLM interactions

## Structure

```
.context/
├── README.md              # This file
├── context-update.md      # How to update context (Elle-inspired)
└── core/                  # Core context files
    ├── identity.md        # Repo identity, mission, purpose
    ├── preferences.md     # Repo-level preferences for agents/humans
    ├── workflows.md       # Repo SOPs (staging, validation, promotion)
    ├── relationships.md   # Stakeholders, roles, collaborators
    ├── triggers.md        # Release gates, recurring audits, deadlines
    ├── projects.md        # Active epics/phases (links to planning/)
    ├── rules.md           # Hard rules (staging-only, no secrets, etc.)
    ├── session.md         # Current session focus
    └── journal.md         # Append-only notable decisions
└── conversations/         # Full conversation transcripts
    ├── README.md          # Transcript naming and redaction rules
    └── [session-id].md    # Individual transcript files
```

## Difference from Other Directories

| Directory | Purpose | Write Policy |
|-----------|---------|--------------|
| `.context/` | Repo memory, transcripts, learnings | Runtime-writable (with rules) |
| `sessions/` | Agent execution history | Runtime-writable |
| `logs/` | Execution logs, errors | Runtime-writable |
| `shared-knowledgebase/` | Cross-agent verified knowledge | Staging + approval required |
| `directives/` | Behavior contracts | Staging + approval required |
| `executions/` | Python tools | Staging + approval required |

## Core Files Explained

| File | Purpose | Example |
|------|---------|---------|
| `identity.md` | Repo mission, scope, goals | "Expert Framework: file-based agentic OS" |
| `preferences.md` | Repo-level preferences | "Always use staging before promotion" |
| `workflows.md` | Standard procedures | "Staging → validation → approval → promotion" |
| `relationships.md` | Stakeholders, roles | "Maintainer: X, Contributors: Y" |
| `triggers.md` | Time-sensitive items | "Release v1.0 by 2025-01-15" |
| `projects.md` | Active work | "Phase 3: Agent instructions (in progress)" |
| `rules.md` | Hard rules | "❌ NEVER write outside staging" |
| `session.md` | Current focus | "Working on Elle integration" |
| `journal.md` | History | "2024-12-23: Completed staging system" |

## Rules System

The `core/rules.md` file is **special** — agents **always check it first** before taking any action. When corrections are made, rules are added so mistakes are never repeated.

Example rules:
```
- ❌ NEVER write to canonical locations without staging
- ✅ ALWAYS check .context/core/rules.md before actions
- ❌ NEVER commit secrets or API keys
- ✅ ALWAYS validate before promotion
```

## Conversation Transcripts

Full transcripts are stored in `.context/conversations/` with:
- Session ID
- Timestamp
- Participants (agent names, user)
- Tools used
- Redaction markers (for secrets)

See `.context/conversations/README.md` for naming conventions and redaction rules.

## Update Policy

Context updates are **autonomous** — agents update context without asking permission, following the "future self" test:

> "If I started a new conversation tomorrow, would this change how I respond?"

Only store information that would change future behavior.

## Loading Context

Agents should load context in this order:
1. **Always first**: `core/rules.md` (hard constraints)
2. **For substantive tasks**: `core/identity.md`, `core/preferences.md`, `core/workflows.md`
3. **For current work**: `core/session.md`
4. **For history**: `core/journal.md` (selective, not full load)
5. **For transcripts**: Only load specific transcripts when needed (they're large)

## Runtime-Writable

Unlike `directives/`, `executions/`, and `shared-knowledgebase/`, `.context/` is **runtime-writable**:
- Agents can write session logs directly
- Agents can append to `journal.md` directly
- Agents can update `session.md` directly
- **But**: No secrets, follow structure, append-only for transcripts

## Integration with Staging

- **`.context/` updates**: Direct writes allowed (runtime-writable)
- **Canonical changes**: Must go through `review-approval/` first
- **Transcripts**: Append-only, no modification after creation

## See Also

- `directives/CONTEXT_MEMORY_SYSTEM.md` - Detailed context loading/update protocol
- `AGENTIC_WORKFLOW_CONTRACT.md` - System contract including `.context/` permissions
- `planning/WORKSESSION_STATE.md` - Current session state (complements `core/session.md`)

