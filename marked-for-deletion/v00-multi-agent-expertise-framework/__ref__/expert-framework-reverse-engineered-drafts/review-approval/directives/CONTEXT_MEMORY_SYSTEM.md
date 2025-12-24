---
directive_id: CONTEXT_MEMORY_SYSTEM
version: 1.0
enforcement_level: MANDATORY
applies_to: ALL_AGENTS
bypass_allowed: false
validation_checkpoint: PRE_EXECUTION
---

### WHAT THIS DIRECTIVE DOES
Enforces the repo-context memory system (`.context/`) to ensure agents and humans never start from scratch. Specifies load order, update triggers, and interaction with progressive loading.

### ORCHESTRATOR EXECUTION SEQUENCE

**CHECKPOINT 1: Rules-First Load (MANDATORY)**
```
BEFORE {{AGENT_NAME}} takes ANY action:
  
  REQUIRED_ACTION:
    - Read {{.context/core/rules.md}} FIRST
    - Check for rules that apply to intended action
    - If rule conflicts with action: STOP and ask user
  
  ENFORCEMENT:
    IF agent takes action without checking rules.md:
      REJECT_ACTION
      RETURN: "Must check .context/core/rules.md before any action"
```

**CHECKPOINT 2: Context Loading (Progressive)**
```
FOR substantive tasks (not just "what tools do you have?"):
  
  REQUIRED_ACTION:
    - Load core context files:
      1. {{.context/core/rules.md}} (always first)
      2. {{.context/core/identity.md}} (repo mission)
      3. {{.context/core/preferences.md}} (repo preferences)
      4. {{.context/core/workflows.md}} (repo SOPs)
      5. {{.context/core/session.md}} (current focus)
  
  OPTIONAL_LOAD (on-demand):
    - {{.context/core/projects.md}} (if working on specific project)
    - {{.context/core/relationships.md}} (if stakeholders relevant)
    - {{.context/core/triggers.md}} (if time-sensitive items relevant)
    - {{.context/core/journal.md}} (if history needed, selective load only)
  
  FORBIDDEN:
    - Loading all transcripts from {{.context/conversations/}} upfront
    - Loading entire journal.md (selective entries only)
  
  ENFORCEMENT:
    IF agent loads all transcripts or full journal:
      WARN: "Context bloat detected"
      LOG: violation to {{CONTEXT_VIOLATIONS_LOG}}
```

**CHECKPOINT 3: Session Context Update**
```
DURING session:
  
  REQUIRED_ACTION:
    - Update {{.context/core/session.md}} with:
      • Current focus
      • Active tasks
      • Blockers
      • Notes for next session
  
  UPDATE_FREQUENCY:
    - At session start: Initialize session.md
    - During session: Update as focus changes
    - At session end: Finalize notes for next session
  
  ENFORCEMENT:
    IF session.md not updated during session:
      WARN: "Session context not maintained"
```

**CHECKPOINT 4: Correction Detection (Self-Improvement)**
```
WHEN user corrects behavior:
  
  REQUIRED_ACTION:
    - IMMEDIATELY add rule to {{.context/core/rules.md}}
    - Use format: ❌ NEVER [action] or ✅ ALWAYS [action]
    - Include reason/origin if helpful
  
  REQUIRED_OUTPUT:
    - Rule added to rules.md
    - Brief notification: "Added rule: [rule text]"
  
  ENFORCEMENT:
    IF correction detected but rule not added:
      MARK_INCOMPLETE
      RETURN: "Corrections must be added to rules.md immediately"
```

**CHECKPOINT 5: Journal & Transcript Creation**
```
AFTER notable session:
  
  REQUIRED_ACTION:
    - Append entry to {{.context/core/journal.md}} (at TOP, newest first)
    - Create transcript in {{.context/conversations/[session-id]-[timestamp].md}}
    - Include frontmatter: session_id, timestamp, participants, tools_used, redactions
    - Include full transcript content (user preference)
    - Redact secrets: use [REDACTED: reason] markers
  
  REQUIRED_OUTPUT:
    - Journal entry (brief summary)
    - Transcript file (full conversation)
    - Redaction log in transcript frontmatter
  
  ENFORCEMENT:
    IF transcript created but secrets not redacted:
      REJECT_TRANSCRIPT
      RETURN: "Secrets must be redacted before creating transcript"
```

**CHECKPOINT 6: Preference/Workflow Learning**
```
WHEN new preference or workflow learned:
  
  REQUIRED_ACTION:
    - Update {{.context/core/preferences.md}} or {{.context/core/workflows.md}}
    - REPLACE old preference if contradicts (don't accumulate)
    - Brief notification: "Noted preference for X"
  
  ENFORCEMENT:
    IF contradictory preferences accumulate:
      WARN: "Contradictory preferences detected"
      ASK_USER: "Which preference is current?"
```

### LOAD ORDER (MANDATORY)

**Always Load First:**
1. `.context/core/rules.md` - Hard constraints (check before ANY action)

**For Substantive Tasks:**
2. `.context/core/identity.md` - Repo mission and scope
3. `.context/core/preferences.md` - Repo-level preferences
4. `.context/core/workflows.md` - Standard procedures
5. `.context/core/session.md` - Current focus

**On-Demand Only:**
6. `.context/core/projects.md` - If working on specific project
7. `.context/core/relationships.md` - If stakeholders relevant
8. `.context/core/triggers.md` - If time-sensitive items relevant
9. `.context/core/journal.md` - Selective entries only (not full file)
10. `.context/conversations/[specific-session].md` - Only when specific transcript needed

### UPDATE TRIGGERS

| Trigger | Action | File |
|---------|--------|------|
| Session starts | Initialize session.md | `.context/core/session.md` |
| Focus changes | Update session.md | `.context/core/session.md` |
| User corrects behavior | Add rule immediately | `.context/core/rules.md` |
| New preference stated | Replace old preference | `.context/core/preferences.md` |
| Workflow learned | Update workflows | `.context/core/workflows.md` |
| Project status changes | Update projects | `.context/core/projects.md` |
| Notable session ends | Append journal entry | `.context/core/journal.md` |
| Session ends | Create transcript | `.context/conversations/[id].md` |

### INTERACTION WITH PROGRESSIVE LOADING

**Integration with `directives/PROGRESSIVE_LOADING.md`:**

- **Level 1 (Front Matter)**: Load `.context/core/rules.md` frontmatter only
- **Level 2 (Full Instructions)**: Load core context files (identity, preferences, workflows, session)
- **Level 3 (Reference Files)**: Load specific journal entries or transcripts on-demand
- **Level 4 (Execute Tools)**: Use execution tools, don't load code

**Context Budget:**
- Core context files: ~2000 tokens total
- Journal entries: < 500 tokens per entry (load selectively)
- Transcripts: Large (excluded from default context, load on-demand only)

### FORBIDDEN ACTIONS

- ❌ Taking action without checking `.context/core/rules.md` first
- ❌ Loading all transcripts upfront (context bloat)
- ❌ Loading entire journal.md (selective entries only)
- ❌ Creating transcripts with secrets (must redact)
- ❌ Modifying transcripts after creation (append-only)
- ❌ Accumulating contradictory preferences (replace old)

### VALIDATION CRITERIA

Directive is SUCCESSFUL when:
- ✓ Rules checked before every action
- ✓ Core context loaded for substantive tasks
- ✓ Session context maintained throughout session
- ✓ Corrections immediately added to rules.md
- ✓ Transcripts created after each session (with redactions)
- ✓ No context bloat (transcripts not loaded by default)
- ✓ Progressive loading respected (selective journal/transcript loading)

