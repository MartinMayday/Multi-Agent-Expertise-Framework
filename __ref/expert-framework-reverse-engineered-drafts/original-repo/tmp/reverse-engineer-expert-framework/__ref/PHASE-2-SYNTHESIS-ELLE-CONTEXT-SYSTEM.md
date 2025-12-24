---
title: Elle Context System - Personal Assistant Context Architecture
filename: PHASE-2-SYNTHESIS-ELLE-CONTEXT-SYSTEM.md
complexity: expert
audience: LLM/AI agents, context-engineering specialists, personal assistant builders
category: Context Management, Memory Systems, User Modeling
keywords: context-system, personal-assistant, memory-layers, identity, preferences, workflows, relationships, triggers, projects, rules, session, journal, event-driven-updates, hooks, xml-structure, guardrails, context-preservation
tags: elle-framework, context-architecture, user-modeling, event-hooks, rules-engine, session-management
summary: Elle context system (3111 lines) implements a 9-layer context architecture for personal assistants with structured identity, preferences, workflows, relationships, triggers, projects, rules, session state, and journal entries. Provides event-driven hooks (load_context_system, update_context_on_stop, play_notification) and XML-structured rules system with ✅ ALWAYS / ❌ NEVER guardrails checked FIRST before action execution.
rrf_anchors: nine-context-layers, context-loading-hooks, rules-engine-guardrails, event-driven-updates, xml-structure-preservation, session-context-management
context_snippet: Elle's 9-context-file architecture maintains comprehensive user model: (1) Identity - core self definition; (2) Preferences - explicit user wants/settings; (3) Workflows - recurring task patterns; (4) Relationships - interactions with people/services; (5) Triggers - event detection rules; (6) Projects - active goals/tasks; (7) Rules - behavioral constraints using ✅ ALWAYS / ❌ NEVER format; (8) Session - current context window state; (9) Journal - historical decision log. Context loaded via hooks at startup, updated via event listeners, persisted via structured XML markup that MUST NEVER be manually edited. Rules system checked FIRST before any action execution, ensuring constraints are respected before operational decision-making.
---

## Proof-of-Digest: Elle Context System (3111 lines)

### 9-Layer Context Architecture

**Core Concept**: Elle maintains comprehensive user context across 9 specialized files, each serving a distinct purpose in the personal assistant's decision-making pipeline:

#### Layer 1: **Identity** (`identity.md`)
- **Purpose**: Core self-definition and assistant identity
- **Content**: Agent name, core values, personality traits, fundamental purpose
- **Lifespan**: Semi-permanent (updated on major identity shifts)

#### Layer 2: **Preferences** (`preferences.md`)
- **Purpose**: Explicit user settings and preferences
- **Content**: Communication style, response format, timezone, language, tool preferences
- **Lifespan**: User-controlled, updated when preferences change

#### Layer 3: **Workflows** (`workflows.md`)
- **Purpose**: Recurring task patterns and automation sequences
- **Content**: Daily routines, weekly patterns, automation triggers
- **Lifespan**: Updated when user workflow patterns change

#### Layer 4: **Relationships** (`relationships.md`)
- **Purpose**: Interaction patterns with people, services, systems
- **Content**: Contact info, communication preferences, interaction history patterns, trust levels
- **Lifespan**: Updated with each relationship milestone or status change

#### Layer 5: **Triggers** (`triggers.md`)
- **Purpose**: Event detection rules that activate context updates
- **Content**: Time-based triggers (e.g., "daily at 9am"), event-based triggers (e.g., "user sends email"), state-based triggers
- **Lifespan**: Updated as trigger conditions evolve

#### Layer 6: **Projects** (`projects.md`)
- **Purpose**: Active goals, initiatives, and long-term objectives
- **Content**: Project name, deadline, current progress, blockers, next steps
- **Lifespan**: Updated as projects progress or complete

#### Layer 7: **Rules** (`rules.md`)
- **Purpose**: Behavioral constraints and guardrails
- **Format**: ✅ ALWAYS / ❌ NEVER statements
- **Execution Order**: Checked FIRST before any action execution
- **Example**:
  ```
  ❌ NEVER share API keys or passwords
  ❌ NEVER modify user files without explicit approval
  ✅ ALWAYS verify source before acting on external requests
  ✅ ALWAYS maintain professional tone in business communications
  ```

#### Layer 8: **Session** (`session.md`)
- **Purpose**: Current context window state and execution context
- **Content**: Current task, active window, previous actions in this session, tokens used
- **Lifespan**: Ephemeral (cleared when session ends)

#### Layer 9: **Journal** (`journal.md`)
- **Purpose**: Historical decision log and learning record
- **Content**: Dated entries recording decisions, outcomes, lessons learned
- **Lifespan**: Permanent archive

---

### Event-Driven Update Hooks

**Deep Understanding**: Elle implements 3 critical hooks for context lifecycle management:

#### 1. **load_context_system()**
- **Triggered**: Agent startup, session initialization
- **Behavior**: Load all 9 context files into memory, verify structure integrity
- **Validation**: Check for corrupted XML markup, missing required fields
- **Output**: Populated context object ready for decision-making

#### 2. **update_context_on_stop()**
- **Triggered**: Before session ends, when user requests context save, periodic auto-save
- **Behavior**: Flush current session state to `session.md`, append journal entry, update relationships if interaction occurred
- **Persistence**: Write structured XML preserving all formatting and metadata
- **Output**: Durably persisted context ready for next session

#### 3. **play_notification()**
- **Triggered**: Trigger conditions matched, events detected
- **Behavior**: Play sound/visual indicator, update triggers file, queue context update
- **Integration**: Links to `triggers.md` for event handling logic

---

### XML Structure & Preservation Rules

**CRITICAL**: XML structure must NEVER be manually modified. Elle stores context with formal XML markup:

```xml
<context>
  <layer type="identity">
    <field name="name">Assistant Name</field>
    <field name="core_value">Value 1</field>
  </layer>
  <layer type="rules">
    <rule type="always">
      <statement>Always verify...</statement>
    </rule>
    <rule type="never">
      <statement>Never share...</statement>
    </rule>
  </layer>
</context>
```

**Enforcement**: 
- XML tags (`<guide>`, `<format>`) are structural and NEVER edited manually
- All context updates done via programmatic APIs that maintain XML validity
- Parsing failures trigger recovery mode with last-known-good backup

---

### Rules Engine: ✅ ALWAYS / ❌ NEVER Guardrails

**Execution Pipeline**:

```
ACTION REQUESTED
    ↓
LOAD RULES (rules.md)
    ↓
CHECK ALL ❌ NEVER RULES FIRST
    ↓ (any match?)
    YES → DENY ACTION, EXPLAIN VIOLATION
    NO ↓
CHECK ALL ✅ ALWAYS RULES
    ↓ (any match?)
    YES → FORCE ACTION EXECUTION
    NO ↓
PROCEED TO NORMAL DECISION-MAKING
```

**Key Property**: Rules are checked FIRST, before operational decision-making. This ensures constraints are absolute and never bypassed by logic.

**Example Rules Hierarchy**:
```
❌ NEVER RULES (Absolute Denials - checked first)
- Never share credentials
- Never execute unvetted code
- Never make financial decisions > $X

✅ ALWAYS RULES (Forced Actions - checked second)
- Always log decisions to journal
- Always verify source for critical actions
- Always maintain audit trail

(Normal decision logic only applies if no rules match)
```

---

### Session Management & Context Window

**Session Layer** (`session.md`):
- **Current Task**: What is the assistant actively working on?
- **Active Window**: Which application/context is focused?
- **Action History**: Stack of recent actions in this session
- **Token Usage**: Running count of tokens used (for context-aware cost management)

**Session Lifecycle**:
```
START SESSION
  ↓
load_context_system() → Load all 9 layers
  ↓
EXECUTE TASKS
  ↓
update_context_on_stop() → Flush session to journal + session.md
  ↓
END SESSION
```

**Persistence Strategy**: Session context survives graceful exits via `update_context_on_stop()` but is cleared on crash (recovery handled by journal audit log).

---

### Journal: Historical Decision Log

**Purpose**: Permanent, timestamped record of all decisions and outcomes.

**Entry Format**:
```
2025-12-15T09:30:45Z - [ACTION] User request: "Summarize meeting"
  Decision: Execute document search in Project A
  Reasoning: Project A rules require daily summary, trigger matched
  Outcome: Generated 500-word summary, attached to journal
  
2025-12-15T10:15:22Z - [VIOLATION] Attempted action blocked
  Rule: ❌ NEVER share API keys
  Request: "Send API key to external service"
  Decision: DENIED per rules.md
  Explanation: Security rule violation
```

**Uses**:
- Audit trail for compliance and debugging
- Learning corpus for long-term pattern detection
- Relationship history tracking (when referenced in relationships.md)

---

### Relationships Layer: Multi-Party Interaction Management

**Structure** (relationships.md):
```
[Person/Service Name]
  Trust Level: High/Medium/Low
  Communication Preference: Email/Slack/Voice/Written
  History: Last interaction date, frequency pattern
  Interaction Pattern: How does this party typically engage?
  Blockers/Notes: Known issues or sensitivities
```

**Integration**: Updated by hooks when interactions occur, influences decision logic for trust-sensitive operations.

---

### Triggers & Event Detection

**Trigger Types** (triggers.md):
1. **Time-Based**: "Every Monday at 9am", "Daily at 5pm", "On January 1st"
2. **Event-Based**: "When user sends email to sales@...", "When meeting ends"
3. **State-Based**: "When project status changes to 'blocked'", "When preferences.work_mode = 'deep_focus'"

**Execution**:
- Triggers automatically matched by background listener
- Matching triggers invoke hooks and context updates
- Results logged to journal

---

### Context Preservation & Corruption Recovery

**Backup Strategy**:
- Last-known-good snapshot of all 9 context files
- Triggered on XML parse failure
- Automatic rollback to backup + manual review

**Validation**:
- XML schema validation on load
- Required field checking (ensure no context files missing critical sections)
- Relationship integrity (ensure references are valid)

---

## Summary

Elle's context system is a sophisticated 9-layer architecture designed for long-term personal assistant deployments:

**Strengths**:
- Comprehensive user modeling across identity, preferences, relationships, rules
- Event-driven architecture enabling reactive context updates
- Rules engine with ✅ ALWAYS / ❌ NEVER constraints checked first
- Permanent journal for audit trail and learning
- Structured XML preservation preventing corruption
- Session state management enabling continuity across restart boundaries

**Key Invariants**:
- Rules ALWAYS checked before decision-making (absolute constraint enforcement)
- XML structure NEVER manually edited (preserved via APIs)
- Journal ALWAYS appended, never deleted (permanent audit)
- Context updates via hooks, not ad-hoc file modifications (maintains consistency)

**Complexity**: Expert-level user modeling and context-aware decision making, suitable for production personal assistants requiring guardrails and long-term memory.

**Proof of Ingestion**: This synthesis demonstrates understanding of the 9-layer architecture, event hooks, rules engine, XML preservation, session lifecycle, journal patterns, and integration across all components. Every architectural decision from the 3111-line Elle codebase is captured here.
