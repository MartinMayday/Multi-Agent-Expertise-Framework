---
directive_id: PROGRESSIVE_LOADING
version: 1.0
enforcement_level: MANDATORY
applies_to: ALL_AGENTS
bypass_allowed: false
validation_checkpoint: CONTEXT_LOADING
---

### WHAT THIS DIRECTIVE DOES
Prevents context window bloat by loading documentation in stages. Reduces costs, improves focus, enables scaling.

### ORCHESTRATOR EXECUTION SEQUENCE

**LEVEL 1: Front Matter (Always Loaded)**
```
ON agent invocation:
  
  AUTO_LOAD:
    - {{AGENT_SYSTEM_INSTRUCTIONS_MD}} frontmatter only
    - {{KB_MANIFEST_MD}} quick reference section only
    - {{DIRECTIVES_LIST}} (names only, not full content)
  
  EXPECTED_CONTEXT_SIZE:
    - Target: < 500 tokens
    - Purpose: Answer "Should I use this skill/knowledge?"
  
  ENFORCEMENT:
    IF context > 500 tokens at L1:
      WARN: "Front matter too verbose"
```

**LEVEL 2: Full Instructions (On-Demand)**
```
WHEN agent decides skill is relevant:
  
  REQUIRED_ACTION:
    - Ask user: "Load {{SKILL_NAME}}? ({{TOKEN_ESTIMATE}} tokens)"
    - IF approved: Load {{AGENT_SYSTEM_INSTRUCTIONS_MD}} full content
  
  CONTEXT_BUDGET:
    - Target: < 2000 tokens
    - Purpose: Understand complete workflow
  
  ENFORCEMENT:
    IF agent loads without user confirmation:
      WARN: "Unauthorized L2 load"
      LOG: violation to {{CONTEXT_VIOLATIONS_LOG}}
```

**LEVEL 3: Reference Files (Selectively Loaded)**
```
WHEN agent needs detailed documentation:
  
  REQUIRED_PATTERN:
    - Agent identifies {{KNOWLEDGE_GAP}}
    - Checks {{KB_MANIFEST_MD}} for relevant snippet
    - Loads ONLY {{SPECIFIC_SNIPPET_MD}}
    - NOT entire knowledge base
  
  CONTEXT_BUDGET:
    - Per snippet: < 1500 tokens
    - Max simultaneous: {{MAX_SNIPPETS}} (default: 3)
  
  ENFORCEMENT:
    IF agent loads > {{MAX_SNIPPETS}}:
      FORCE_UNLOAD oldest snippet
      LOG: "Context budget exceeded"
```

**LEVEL 4: Source Code (Execute, Don't Load)**
```
WHEN agent needs computation:
  
  REQUIRED_PATTERN:
    - Read {{EXECUTIONS_README_MD}} to find tool
    - Execute {{PYTHON_TOOL_PATH}} with {{INPUT_PARAMS}}
    - Receive {{OUTPUT_ONLY}} (code stays external)
  
  CONTEXT_IMPACT:
    - Tool code: NOT loaded into context
    - Tool output: Loaded (typically < 500 tokens)
  
  ENFORCEMENT:
    Agent sees: input → [black box] → output
    Agent never sees: tool implementation details
```

### CONTEXT BUDGET ENFORCEMENT
```
GLOBAL_LIMITS:
  
  MAX_CONTEXT_WINDOW:
    - Per agent invocation: {{MAX_TOKENS}} (default: 15000)
    - Progressive loading overhead: {{OVERHEAD_TOKENS}} (default: 2000)
    - Available for task: {{MAX_TOKENS - OVERHEAD_TOKENS}}
  
  MONITORING:
    - Track: {{CURRENT_CONTEXT_SIZE}}
    - Alert at: {{WARNING_THRESHOLD}}% (default: 80%)
    - Halt at: {{MAX_THRESHOLD}}% (default: 95%)
  
  ENFORCEMENT:
    IF context exceeds {{MAX_THRESHOLD}}:
      FORCE_UNLOAD least-recently-used content
      PRIORITIZE: directives > KB snippets > examples
```

### LOADING DECISION TREE
```
Agent asks: "Do I need X?"

DECISION_PROCESS:
  
  OPTION_1: Already in Context
    → Use it immediately
  
  OPTION_2: Available in Manifest (L1)
    → Relevant to task? Load L2
  
  OPTION_3: Not in Context, Check Manifest
    → Load specific snippet (L3)
  
  OPTION_4: Requires Computation
    → Execute tool (L4), don't load code
  
  OPTION_5: Not Available Anywhere
    → Return to MetaGPT: "Missing: {{WHAT}}"
```

### UNLOADING STRATEGY
```
WHEN context budget tight:
  
  PRIORITIZED_RETENTION:
    1. {{DIRECTIVES}} (KB_GUARDRAILS, HANDOFF_PROTOCOL, etc.)
    2. {{AGENT_SYSTEM_INSTRUCTIONS}}
    3. {{CURRENT_TASK_CONTEXT}}
    4. {{ACTIVE_KB_SNIPPETS}}
    5. {{EXAMPLES}} (unload first if needed)
  
  ENFORCEMENT:
    Never unload items 1-3
    Unload items 4-5 in reverse priority order
```

### VALIDATION CRITERIA
```
Directive is SUCCESSFUL when:
  ✓ Context stays under budget consistently
  ✓ Agents load only what they need
  ✓ Performance remains fast
  ✓ Costs are minimized

Directive FAILED when:
  ✗ Context regularly exceeds limits
  ✗ Agents load entire KB upfront
  ✗ Response times increase
  ✗ Token usage spikes
```

### DEPLOYMENT INSTRUCTIONS
```
1. Save as: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/directives/PROGRESSIVE_LOADING.md
2. Reference in: ALL agent {{SYSTEM_INSTRUCTIONS_MD}} files
3. Enforcement by: Context manager (built-in to orchestrator)
4. Monitor via: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/sessions/context_metrics.json
5. Configure limits in: /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/.env
   - MAX_CONTEXT_WINDOW={{TOKEN_LIMIT}}
   - WARNING_THRESHOLD={{PERCENT}}
   - MAX_SNIPPETS={{COUNT}}
```
