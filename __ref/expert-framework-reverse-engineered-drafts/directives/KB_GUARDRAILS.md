---
directive_id: KB_GUARDRAILS
version: 1.0
enforcement_level: MANDATORY
applies_to: ALL_AGENTS
bypass_allowed: false
validation_checkpoint: PRE_EXECUTION
---

### WHAT THIS DIRECTIVE DOES
Prevents agents from producing responses based on assumptions. Forces documentation-first workflow through mandatory knowledge base checks.

### ORCHESTRATOR EXECUTION SEQUENCE

**CHECKPOINT 1: KB Gate Entry**
```
BEFORE {{AGENT_NAME}} processes {{USER_REQUEST}}:
  
  REQUIRED_ACTION:
    - Read {{KB_MANIFEST_PATH}}
    - Read {{AGENT_KB_MANIFEST_PATH}}
  
  REQUIRED_OUTPUT:
    - KB_STATUS: {{sufficient|partial|insufficient}}
  
  ENFORCEMENT:
    IF KB_STATUS == undeclared:
      HALT_EXECUTION
      RETURN: "Agent must declare KB sufficiency status"
```

**CHECKPOINT 2: Insufficiency Handler**
```
IF KB_STATUS == "insufficient" OR KB_STATUS == "partial":
  
  REQUIRED_ACTION:
    - Identify {{MISSING_INFORMATION}}
    - Document {{WHY_BLOCKS_PROGRESS}}
  
  REQUIRED_OUTPUT:
    - Stop execution immediately
    - Present to user:
      • What is missing: {{MISSING_INFORMATION}}
      • Why it blocks: {{WHY_BLOCKS_PROGRESS}}
      • Approval needed: {{yes|no}}
  
  ENFORCEMENT:
    Agent CANNOT proceed to research without explicit user approval
```

**CHECKPOINT 3: Research Gate**
```
IF user_approval == true:
  
  REQUIRED_ACTION:
    - Execute {{RESEARCH_METHOD}} using {{MCP_TOOLS_DECLARED}}
    - Track {{SOURCE_URL}} for every factual claim
    - Prefer {{OFFICIAL_DOCS}} over {{SECONDARY_SOURCES}}
  
  REQUIRED_OUTPUT:
    - Research findings with source attribution
    - Confidence scoring per finding
  
  ENFORCEMENT:
    IF claim has no source:
      REJECT_CLAIM
      LOG: "Unsourced claim removed"
```

**CHECKPOINT 4: KB Write-Back**
```
AFTER research completion:
  
  REQUIRED_ACTION:
    - Generate {{NEW_KB_SNIPPETS}} in standard format
    - OR propose {{KB_SNIPPET_UPDATES}} to existing entries
  
  REQUIRED_OUTPUT:
    - Ready-to-save KB snippet(s)
    - Update location: {{KB_PATH}}
    - Frontmatter metadata complete
  
  ENFORCEMENT:
    IF no KB update proposed:
      MARK_TASK_INCOMPLETE
      RETURN: "Research without KB update is invalid"
```

**CHECKPOINT 5: Task Output**
```
ONLY AFTER all checkpoints pass:
  
  REQUIRED_ACTION:
    - Produce {{TASK_OUTPUT}}
    - Cite {{KB_SNIPPET_IDS}} used
  
  REQUIRED_OUTPUT:
    - Primary response
    - KB snippet references
    - Source traceability
```

### FAILURE HANDLING
```
AT ANY CHECKPOINT:
  IF agent cannot proceed safely:
    
    REQUIRED_ACTION:
      - Emit HANDOFF block to {{METAGPT}}
      - Status: {{blocked}}
      - Missing: {{REQUIRED_INPUT}}
    
    ENFORCEMENT:
      MetaGPT evaluates: {{retry|ask_user|terminate}}
```

### VALIDATION CRITERIA
```
Directive is SUCCESSFUL when:
  ✓ No agent response contains undocumented facts
  ✓ All research updates KB
  ✓ KB grows on every session
  ✓ Source traceability is maintained

Directive FAILED when:
  ✗ Agent produces unsourced claims
  ✗ Research happens without user approval
  ✗ KB remains unchanged after research
  ✗ Agent proceeds with "insufficient" KB status
```

### DEPLOYMENT INSTRUCTIONS
```
1. Save as: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/directives/KB_GUARDRAILS.md
2. Reference in: ALL agent {{SYSTEM_INSTRUCTIONS_MD}} files
3. Enforcement by: {{METAGPT}} pre-execution validation
4. Log violations to: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/sessions/kb_violations.log
```
