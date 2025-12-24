---
directive_id: FAILURE_HANDLING
version: 1.0
enforcement_level: MANDATORY
applies_to: ALL_AGENTS
bypass_allowed: false
validation_checkpoint: ERROR_DETECTION
---

### WHAT THIS DIRECTIVE DOES
Makes failure a first-class outcome. Prevents silent errors, enables graceful degradation, maintains system trust.

### ORCHESTRATOR EXECUTION SEQUENCE

**FAILURE DETECTION**
```
AGENT MUST detect these failure conditions:
  
  FAILURE_TYPE_1: Insufficient Information
    - KB incomplete
    - Documentation missing
    - Context inadequate
  
  FAILURE_TYPE_2: Tool Unavailable
    - MCP server unresponsive
    - Required tool not declared
    - Execution timeout
  
  FAILURE_TYPE_3: Constraint Violation
    - Cannot meet requirements
    - Conflicting instructions
    - Resource limits exceeded
  
  FAILURE_TYPE_4: Validation Failed
    - Output doesn't meet criteria
    - Tests failed
    - Quality threshold not met

ENFORCEMENT:
  IF agent detects failure:
    MUST NOT attempt workaround without explicit approval
    MUST NOT produce partial/incorrect output
    MUST halt and report
```

**FAILURE REPORTING**
```
WHEN failure detected:
  
  REQUIRED_REPORT_FORMAT:
    {
      "failure_id": "{{UNIQUE_ID}}",
      "agent": "{{AGENT_NAME}}",
      "task": "{{TASK_DESCRIPTION}}",
      "timestamp": "{{ISO_8601_TIMESTAMP}}",
      
      "failure_type": "{{TYPE_FROM_ABOVE}}",
      
      "failure_details": {
        "what_failed": "{{SPECIFIC_FAILURE}}",
        "at_step": "{{WORKFLOW_STEP}}",
        "error_message": "{{ERROR_TEXT}}"
      },
      
      "root_cause": "{{ANALYSIS}}",
      
      "attempted_recovery": [
        {
          "action": "{{WHAT_WAS_TRIED}}",
          "result": "{{SUCCESS|FAILURE}}"
        }
      ],
      
      "required_to_proceed": "{{WHAT_IS_NEEDED}}",
      
      "severity": "{{low|medium|high|critical}}",
      
      "user_action_required": {{true|false}},
      
      "safe_to_retry": {{true|false}},
      
      "suggested_alternative": "{{FALLBACK_APPROACH|null}}"
    }

ENFORCEMENT:
  IF failure report incomplete:
    Escalate to MetaGPT for investigation
```

**FAILURE ESCALATION**
```
SEVERITY_BASED_ROUTING:
  
  LOW_SEVERITY:
    - Agent logs warning
    - Continues with degraded functionality
    - Example: Optional formatting unavailable
  
  MEDIUM_SEVERITY:
    - Agent pauses execution
    - Reports to MetaGPT
    - Awaits decision: retry|fallback|user_input
    - Example: Secondary data source unavailable
  
  HIGH_SEVERITY:
    - Agent halts immediately
    - Handoff to MetaGPT with full context
    - User notification required
    - Example: KB validation failed
  
  CRITICAL_SEVERITY:
    - Entire workflow halts
    - System state preserved
    - User intervention mandatory
    - Example: Data corruption detected
```

**RECOVERY STRATEGIES**
```
STRATEGY_1: Automatic Retry
  WHEN: Transient failures (network, timeout)
  MAX_ATTEMPTS: {{RETRY_LIMIT}} (default: 3)
  BACKOFF: Exponential (1s, 2s, 4s)
  ENFORCEMENT: Log each attempt

STRATEGY_2: Fallback Mode
  WHEN: Primary method unavailable
  REQUIRES: Predefined fallback in {{AGENT_CONFIG}}
  EXAMPLE: web.search fails → use local cache
  ENFORCEMENT: Document quality tradeoff

STRATEGY_3: Graceful Degradation
  WHEN: Non-critical feature unavailable
  REQUIRES: Core functionality remains intact
  EXAMPLE: Syntax highlighting off, but code generation works
  ENFORCEMENT: Inform user of limitations

STRATEGY_4: User Escalation
  WHEN: No automatic recovery possible
  REQUIRES: Clear question to user
  EXAMPLE: "Choose data source: A or B?"
  ENFORCEMENT: Pause until user responds

STRATEGY_5: Workflow Termination
  WHEN: Fundamental requirement cannot be met
  REQUIRES: Preserve all work done so far
  EXAMPLE: Required API credentials missing
  ENFORCEMENT: Save state, clean exit
```

**FAILURE LEARNING**
```
AFTER failure resolution:
  
  REQUIRED_ACTIONS:
    - Log to: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/eval/failure_analysis.md
    - Include:
      • What failed
      • Why it failed
      • How it was resolved
      • How to prevent recurrence
    
    - Update agent's {{MATURITY_SCORE}}:
      • Decrease on repeated failures
      • Increase on successful recovery
    
    - Propose KB update:
      • Add known failure patterns
      • Document workarounds
      • Update troubleshooting guides

ENFORCEMENT:
  Failures without post-mortem analysis are incomplete
```

**FAILURE PREVENTION**
```
PROACTIVE_CHECKS:
  
  BEFORE_EXECUTION:
    - Validate {{REQUIRED_TOOLS}} available
    - Check {{KB_STATUS}} adequate
    - Confirm {{USER_INPUT}} complete
  
  DURING_EXECUTION:
    - Monitor {{CONTEXT_BUDGET}}
    - Track {{EXECUTION_TIME}}
    - Validate {{INTERMEDIATE_OUTPUTS}}
  
  AFTER_EXECUTION:
    - Run {{VALIDATION_TESTS}}
    - Check {{OUTPUT_QUALITY}}
    - Verify {{KB_UPDATES_COMPLETE}}
```

### TRUST MAINTENANCE
```
HONESTY_REQUIREMENTS:
  
  AGENT MUST:
    ✓ Admit when information is unavailable
    ✓ Report limitations clearly
    ✓ Never fabricate data to complete task
    ✓ Distinguish facts from assumptions
  
  AGENT MUST NOT:
    ✗ Silently skip steps
    ✗ Return partial results as complete
    ✗ Hide errors
    ✗ Guess instead of research
```

### VALIDATION CRITERIA
```
Directive is SUCCESSFUL when:
  ✓ Failures are detected early
  ✓ Failure reports are actionable
  ✓ Recovery happens automatically when possible
  ✓ Users are informed of issues promptly
  ✓ System learns from failures

Directive FAILED when:
  ✗ Silent failures occur
  ✗ Partial/incorrect outputs produced
  ✗ Same failures repeat without learning
  ✗ Users discover errors after handoff
  ✗ Workflow corruption undetected
```

### DEPLOYMENT INSTRUCTIONS
```
1. Save as: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/directives/FAILURE_HANDLING.md
2. Reference in: ALL agent {{SYSTEM_INSTRUCTIONS_MD}} files
3. Enforcement by: {{METAGPT}} error handlers
4. Log failures to: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/sessions/failures/{{FAILURE_ID}}.json
5. Track patterns in: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/eval/failure_analysis.md
6. Configure in: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/.env
   - RETRY_LIMIT={{COUNT}}
   - FAILURE_SEVERITY_THRESHOLD={{LEVEL}}
   - AUTO_RECOVERY_ENABLED={{true|false}}
```



## DEPLOYMENT ORCHESTRATOR CHECKLIST

### Pre-Deployment Validation
```
BEFORE deploying file-based agentic workflow:

[ ] /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts directory created
[ ] {{AGENTIC_WORKFLOW_CONTRACT_MD}} in place
[ ] {{directives/}} folder created
[ ] All 4 core directives saved:
    [ ] KB_GUARDRAILS.md
    [ ] HANDOFF_PROTOCOL.md
    [ ] PROGRESSIVE_LOADING.md
    [ ] FAILURE_HANDLING.md
[ ] {{shared-knowledgebase/}} initialized
[ ] {{agents/}} folder structure ready
[ ] MetaGPT has enforcement authority configured
```

### Configuration Files Required
```
CREATE these in /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts:

.env (global settings)
  MAX_CONTEXT_WINDOW={{TOKEN_LIMIT}}
  RETRY_LIMIT={{COUNT}}
  KB_FIRST_ENFORCEMENT={{true|false}}
  LOGGING_LEVEL={{debug|info|warn|error}}

config.json (system settings)
  {
    "orchestrator": "{{METAGPT}}",
    "directive_enforcement": "strict",
    "progressive_loading": true,
    "failure_handling": "graceful",
    "kb_first": true
  }
```

### Initialization Sequence
```
1. Load AGENTIC_WORKFLOW_CONTRACT.md
2. Load all directives from directives/
3. Initialize MetaGPT with enforcement rules
4. Validate agent definitions exist
5. Check KB manifest accessible
6. Confirm MCP tools configured
7. Start session logging
8. System ready for agent invocation
```

### Health Check Commands
```
VERIFY system operational:

1. Test KB-first enforcement:
   - Invoke agent without KB
   - Expect: Halt with KB insufficiency message

2. Test handoff protocol:
   - Trigger agent transition
   - Expect: Handoff contract emission

3. Test progressive loading:
   - Monitor context size during execution
   - Expect: Context stays within budget

4. Test failure handling:
   - Simulate tool unavailability
   - Expect: Graceful failure report
```



## INTEGRATION INSTRUCTIONS FOR AI/LLM DEPLOYERS

### When Tasked to Deploy This System:

**STEP 1: Scaffold Structure**
```
CREATE directory tree:
  /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/
    agents/
    shared-knowledgebase/
      manifest.md
      snippets/
      frameworks/
    directives/
      KB_GUARDRAILS.md
      HANDOFF_PROTOCOL.md
      PROGRESSIVE_LOADING.md
      FAILURE_HANDLING.md
    sessions/
      workflows/
    .env
    AGENTIC_WORKFLOW_CONTRACT.md
```

**STEP 2: Populate Directives**
```
COPY directive content from this template
REPLACE all {{PLACEHOLDERS}} with:
  - /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts → actual project path
  - {{METAGPT}} → orchestrator agent name
  - {{MAX_TOKENS}} → context limit (e.g., 15000)
  - {{RETRY_LIMIT}} → failure retry count (e.g., 3)
  - {{MAX_SNIPPETS}} → simultaneous KB snippets (e.g., 3)
```

**STEP 3: Configure Enforcement**
```
IN MetaGPT system instructions:
  - Add: "Enforce directives/KB_GUARDRAILS.md"
  - Add: "Enforce directives/HANDOFF_PROTOCOL.md"
  - Add: "Enforce directives/PROGRESSIVE_LOADING.md"
  - Add: "Enforce directives/FAILURE_HANDLING.md"
  - Add: "Reject agent outputs violating contracts"
```

**STEP 4: Validate Deployment**
```
RUN health checks (see above)
VERIFY all checkpoints operational
TEST with simple agent invocation
CONFIRM logging works
```



## SOP TEMPLATE COMPLETE ✅

These 4 directives are:
- **Self-contained** (no external dependencies)
- **Enforceable** (clear checkpoints)
- **Auditable** (logging requirements)
- **IDE/CLI agnostic** (path placeholders)
- **AI/LLM ready** (explicit replacement targets)

**Next**: Deploy scaffold and test with MetaGPT.
