---
directive_id: HANDOFF_PROTOCOL
version: 1.0
enforcement_level: MANDATORY
applies_to: ALL_AGENT_TRANSITIONS
bypass_allowed: false
validation_checkpoint: POST_EXECUTION
---

### WHAT THIS DIRECTIVE DOES
Establishes formal state transfer between agents. Ensures work continuity, prevents state loss, and makes failures explicit.

### ORCHESTRATOR EXECUTION SEQUENCE

**PHASE 1: Pre-Handoff Validation**
```
BEFORE {{AGENT_A}} transfers to {{AGENT_B}}:
  
  REQUIRED_CHECKS:
    - Task objective: {{completed|blocked|failed}}
    - Required artifacts: {{produced|missing}}
    - Assumptions made: {{documented|undocumented}}
  
  ENFORCEMENT:
    IF task objective == "in_progress":
      REJECT_HANDOFF
      RETURN: "Agent must reach terminal state"
```

**PHASE 2: Handoff Contract Emission**
```
{{AGENT_A}} MUST emit:

{
  "handoff_id": "{{UNIQUE_ID}}",
  "from_agent": "{{AGENT_A_NAME}}",
  "to_agent": "{{AGENT_B_NAME|METAGPT}}",
  "timestamp": "{{ISO_8601_TIMESTAMP}}",
  
  "status": "{{success|blocked|failed}}",
  
  "produced_artifacts": [
    {
      "type": "{{file|data|decision}}",
      "location": "{{ARTIFACT_PATH}}",
      "description": "{{BRIEF_DESCRIPTION}}"
    }
  ],
  
  "assumptions": [
    {
      "assumption": "{{ASSUMPTION_TEXT}}",
      "validated": {{true|false}},
      "risk": "{{low|medium|high}}"
    }
  ],
  
  "missing_inputs": [
    {
      "required": "{{INPUT_DESCRIPTION}}",
      "reason": "{{WHY_NEEDED}}",
      "blocking": {{true|false}}
    }
  ],
  
  "recommended_next_agent": "{{AGENT_NAME|USER_INPUT_REQUIRED}}",
  
  "context_summary": "{{ONE_PARAGRAPH_SUMMARY}}",
  
  "kb_updates_proposed": {{true|false}},
  "session_id": "{{SESSION_UUID}}"
}

ENFORCEMENT:
  IF handoff_contract missing any required field:
    REJECT_HANDOFF
    LOG: "Incomplete handoff contract"
```

**PHASE 3: MetaGPT Evaluation**
```
{{METAGPT}} receives handoff contract:
  
  EVALUATION_CRITERIA:
    - Status is terminal: {{completed|blocked|failed}}
    - Artifacts match task objective
    - Assumptions are documented
    - Missing inputs are actionable
  
  DECISION_TREE:
    IF status == "success" AND artifacts_complete:
      → ADVANCE to {{RECOMMENDED_NEXT_AGENT}}
    
    IF status == "blocked" AND missing_inputs_actionable:
      → ASK_USER for {{MISSING_INPUTS}}
    
    IF status == "failed" AND retry_count < {{MAX_RETRIES}}:
      → RETRY with adjusted instructions
    
    IF status == "failed" AND retry_count >= {{MAX_RETRIES}}:
      → TERMINATE workflow with explanation
  
  ENFORCEMENT:
    MetaGPT logs decision rationale to {{WORKFLOW_STATE_JSON}}
```

**PHASE 4: State Transfer**
```
IF handoff approved:
  
  REQUIRED_ACTIONS:
    - Update {{WORKFLOW_STATE_JSON}} with:
      • Previous agent: {{AGENT_A}}
      • Current agent: {{AGENT_B}}
      • Artifacts available: {{ARTIFACT_PATHS}}
      • Context snapshot: {{SUMMARY}}
    
    - Initialize {{AGENT_B}} with:
      • Handoff contract
      • Workflow state
      • Read-only access to {{AGENT_A_SESSIONS}}
  
  ENFORCEMENT:
    {{AGENT_B}} starts with complete context, no assumptions needed
```

**PHASE 5: Handoff Logging**
```
AFTER handoff completion:
  
  REQUIRED_LOGGING:
    - Append to: {{WORKFLOW_DIR}}/handoffs.log
    - Include: handoff_id, from, to, status, timestamp
    - Archive contract to: {{WORKFLOW_DIR}}/handoff_contracts/{{HANDOFF_ID}}.json
  
  ENFORCEMENT:
    All handoffs must be auditable
```

### ROLE ISOLATION ENFORCEMENT
```
STRICT BOUNDARIES:
  
  ResearchGPT:
    ALLOWED: Web search, documentation gathering
    FORBIDDEN: Design decisions, implementation choices
  
  DesignGPT:
    ALLOWED: Architecture, patterns, specifications
    FORBIDDEN: Research, implementation, testing
  
  ImplementationGPT:
    ALLOWED: Code generation from specs
    FORBIDDEN: New design decisions, scope changes

VIOLATION HANDLING:
  IF {{AGENT_X}} performs {{FORBIDDEN_ACTION}}:
    FORCE_HANDOFF to MetaGPT
    LOG: "Role boundary violation"
    REASON: "{{AGENT_X}} attempted {{FORBIDDEN_ACTION}}"
```

### FAILURE HANDLING
```
IF handoff fails:
  
  REQUIRED_ACTIONS:
    - Preserve {{AGENT_A_STATE}} (no data loss)
    - Document {{FAILURE_REASON}}
    - Return control to MetaGPT
    - Offer options:
      • Retry with same agent
      • Assign different agent
      • Request user clarification
      • Terminate workflow gracefully
```

### VALIDATION CRITERIA
```
Directive is SUCCESSFUL when:
  ✓ All agent transitions have handoff contracts
  ✓ No work is lost between transitions
  ✓ Failures are explicit, not silent
  ✓ State is always auditable

Directive FAILED when:
  ✗ Agent transitions without contract
  ✗ State is lost or corrupted
  ✗ Assumptions leak between agents
  ✗ Role boundaries are violated
```

### DEPLOYMENT INSTRUCTIONS
```
1. Save as: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/directives/HANDOFF_PROTOCOL.md
2. Reference in: ALL agent {{SYSTEM_INSTRUCTIONS_MD}} files
3. Enforcement by: {{METAGPT}} at agent transitions
4. State tracking: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/sessions/workflows/{{WORKFLOW_ID}}/state.json
5. Log handoffs to: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/sessions/workflows/{{WORKFLOW_ID}}/handoffs.log
```
