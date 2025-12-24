# Context Update Instructions

This file describes how to maintain the repository's context memory. Update context **continuously** as you learn new things about the repo, its patterns, failures, and successes.

Context updates are **autonomous** — just do them without asking permission.

## Core Principle

> **Only store information that would change how you respond in a future session.**

Context updates are silent housekeeping. Never ask "may I write this down?" Just do it.

## The "Future Self" Test

Before adding ANY context, ask:
> "If I started a new conversation tomorrow, would this change how I respond?"

| ✅ Pass - Add It | ❌ Fail - Skip It |
|------------------|-------------------|
| "Repo uses staging-only writes" | "Ran validation script successfully" |
| "Phase 3 is blocked on agent instructions" | "Created 5 files in review-approval/" |
| "User prefers full transcripts in .context/" | "Session lasted 2 hours" |

## What NEVER Goes in Context

1. **Task completion logs** - "✅ Completed X, ✅ Completed Y" (goes in `sessions/` or `logs/`)
2. **Research summaries** - Store in project docs, reference the path only
3. **Session-specific details** - Goes in `core/session.md` (ephemeral)
4. **Duplicated info** - If it's in project README, don't repeat it
5. **Git history** - If it can be found from `git log`, don't add it
6. **Secrets** - Never, ever, under any circumstances

## Update Steps

### 1. Session Context
Update `.context/core/session.md` with:
- Current focus (what we're working on)
- Active tasks in progress
- Any blockers
- Notes for next session

### 2. Correction Detection (Self-Improvement)
If user corrected any behavior this session, **IMMEDIATELY** add a rule to `.context/core/rules.md`:

| User Says | Interpretation | Add to rules.md |
|-----------|----------------|-----------------|
| "Don't write outside staging" | Explicit instruction | ❌ NEVER write to canonical locations without staging |
| "Why did you skip validation?" | Frustration at action | ❌ NEVER skip validation before promotion |
| "I didn't ask you to create that file" | Unwanted action | ❌ NEVER create files unless necessary |

→ Brief notification: "Added rule: never X without Y"

### 3. Preference/Workflow Learning
If new preference or workflow learned:
→ Update `.context/core/preferences.md` or `.context/core/workflows.md`
→ **REPLACE** old preference if it contradicts (don't accumulate)
→ Brief notification: "Noted preference for X"

### 4. Identity Updates
If new repo identity/mission info learned:
→ Update `.context/core/identity.md`

### 5. Project Status
If project status changed:
→ Update `.context/core/projects.md`
→ Link to `planning/ROADMAP.md` for details

### 6. Relationships
If new stakeholder/role mentioned:
→ Update `.context/core/relationships.md`
→ Include: name, role, relevant context

### 7. Triggers & Important Dates
If important date, deadline, or recurring audit learned:
→ Update `.context/core/triggers.md`
→ Include: date, event/deadline, action needed

### 8. Journal (Session Log)
At the end of notable sessions, append to `.context/core/journal.md`:
→ Date, what was accomplished, notable decisions or context
→ Keep entries brief — anything important should be promoted to relevant core file
→ Add entries at the TOP (newest first)

### 9. Conversation Transcripts
After each session, create transcript in `.context/conversations/`:
→ Use naming convention: `[session-id]-[timestamp].md`
→ Include frontmatter: session_id, timestamp, participants, tools_used, redactions
→ Full transcript content (user opted for full transcripts)
→ **Append-only** — never modify after creation

## File Update Policies

| File | Update Policy |
|------|---------------|
| `core/identity.md` | Update when new identity info shared |
| `core/preferences.md` | **REPLACE** when new preference stated |
| `core/workflows.md` | Update when workflow learned/changed |
| `core/relationships.md` | **ADD** people as mentioned; update context as learned |
| `core/triggers.md` | **ADD** dates/deadlines; remove when passed or irrelevant |
| `core/projects.md` | Update when project status changes; archive completed |
| `core/rules.md` | **ADD** when correction detected; only remove if explicitly rescinded |
| `core/session.md` | Update every session; clear on major context switch |
| `core/journal.md` | **APPEND** notable sessions at TOP; periodically prune old entries |
| `conversations/*.md` | **CREATE** after each session; **NEVER MODIFY** after creation |

## Notification Style

Brief notifications, not permission-seeking:
- ✅ "Done. I've noted the preference for staging-only writes."
- ✅ "Updated session context with current focus."
- ✅ "Added rule: never skip validation."
- ❌ "Would you like me to add this to context?"
- ❌ "Should I update my records?"

## Lifecycle Management

| Type | Action | Trigger |
|------|--------|---------|
| Preferences | **Replace** in place | New preference contradicts old |
| Relationships | **Add** new people; update context | Person mentioned or context learned |
| Triggers | **Add** then **remove** when passed | Date/deadline learned; date passes |
| Projects | **Archive** to bottom section | Project completes |
| Session | **Clear** | Major context switch |
| Journal | **Append** at top; **prune** periodically | Notable session ends; file gets long |
| Rules | **Keep forever** | Only remove on explicit user request |
| Transcripts | **Create** once; **never modify** | Session ends |

## Escalation (Rare)

Only ask the user when there's genuine ambiguity:
1. Contradictory info: "You mentioned preferring X, but I have Y. Which is current?"
2. Rule conflict: "You said never auto-commit, but now asking me to. Update my rules?"
3. Unclear correction: "Was that a correction or situational?"

## Redaction Rules for Transcripts

When creating transcripts in `.context/conversations/`:
- **Never** include API keys, tokens, passwords
- **Never** include personal information (unless explicitly about repo stakeholders)
- **Mark redactions**: Use `[REDACTED: reason]` markers
- **Include redaction log** in frontmatter

## Integration with Staging

- **`.context/` updates**: Direct writes allowed (runtime-writable)
- **Canonical changes**: Must go through `review-approval/` first
- **Transcripts**: Append-only, no modification after creation

