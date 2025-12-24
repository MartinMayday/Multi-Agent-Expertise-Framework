---
title: Expert Framework - Complete File-Based Agentic Orchestration System
filename: FRAMEWORK.md
complexity: expert
audience: Planning AI/LLM agents, platform architects, framework implementers
category: Framework Specification, Orchestration Blueprint, Implementation Guide
keywords: expert-framework, planning-orchestration, file-based-agentic, multi-agent-ensemble, context-engineering, constraint-enforcement, autonomous-execution, directives-execution-knowledge
tags: framework-specification, orchestration-pattern, agentic-workflow, planning-mode
summary: Complete specification for file-based agentic orchestration system independent of IDE/CLI runtime. Combines G3 planning mode (state machine, multi-provider support, autonomous retry), Elle context system (9-layer context architecture with rules-first constraint enforcement), MetaGPT 7-agent pipeline, KB-first guardrails, sequential task chaining, and hybrid search optimization. Supports autonomous AI/LLM orchestration with directives, executions, shared knowledge base, and session tracking.
rrf_anchors: expert-framework-specification, file-based-orchestration, directives-execution-knowledge-trinity, planning-state-machine, rules-first-constraints, autonomous-retry-distribution
context_snippet: Expert Framework implements file-based agentic orchestration through three core subsystems: (1) DIRECTIVES layer specifies intent, workflows, triggers, and constraints; (2) EXECUTIONS layer contains pre-built Python tools/scripts refined via evaluation; (3) SHARED KNOWLEDGE BASE maintains cumulative context, expertise, and learning. Planning state machine manages STARTUP→REFINE→IMPLEMENT→COMPLETE lifecycle. Multi-provider LLM support (Anthropic, OpenAI, Embedded). Elle-inspired 9-layer context ensures identity, preferences, rules, workflows, relationships are maintained. Rules engine enforces ✅ ALWAYS / ❌ NEVER constraints before decision-making. Autonomous retry with 6 attempts over 10 minutes. Sequential task orchestration via directives calling execution tools with TaskOutput gates.
---

# Expert Framework - File-Based Agentic Orchestration Specification

**Version**: 1.0  
**Status**: Ready for Deployment  
**Last Updated**: 2025-12-15  

---

## 1. Overview

The Expert Framework is a complete file-based agentic orchestration system where an AI/LLM acts as orchestrator behavior (follows directives, doesn't code directly). All executions are pre-built Python tools/workflows, refined via evaluation. The system operates independently of IDE/CLI runtime.

**Core Principle**: "Code once, refine via evaluation, execute autonomously"

---

## 2. Architecture: Three Core Subsystems

### 2.1 DIRECTIVES Layer
**Purpose**: Specify intent, workflows, triggers, and constraints

**Location**: `{{PROJECT_ROOT}}/directives/`

**Contents**:
```
directives/
├── README.md                    # Overview of all directives
├── workflows/
│   ├── plan_build_improve.yaml # 3-step workflow: Plan → Build → Self-Improve
│   ├── question_answering.yaml # Answer questions with KB validation
│   └── {{WORKFLOW_NAME}}.yaml  # Your custom workflows
├── triggers/
│   ├── schedule.yaml           # Time-based triggers (cron patterns)
│   ├── event.yaml              # Event-based triggers
│   └── state.yaml              # State-based triggers
├── constraints/
│   ├── rules.md                # ✅ ALWAYS / ❌ NEVER guardrails
│   ├── safety.yaml             # Safety constraints (rate limits, costs)
│   └── compliance.yaml         # Compliance and audit requirements
└── agents/
    ├── planner_directives.md   # Planning agent behavior spec
    ├── executor_directives.md  # Execution agent behavior spec
    └── {{AGENT_NAME}}_directives.md
```

**Directive Format (YAML)**:
```yaml
name: "{{DIRECTIVE_NAME}}"
description: "What this directive does"
type: "workflow|trigger|rule|agent"

# For workflows
steps:
  - step: 1
    action: "execute {{EXECUTION_TOOL_NAME}}"
    inputs: {key: value}
    gate: "await_output"  # Wait for output before next step
    timeout: 300  # seconds
  - step: 2
    action: "execute {{NEXT_EXECUTION_TOOL}}"
    inputs: {path: "{{PREVIOUS_OUTPUT.path}}"}

# For triggers
trigger_type: "schedule|event|state"
condition: "{{CRON_PATTERN}}" or "{{EVENT_PATTERN}}" or "{{STATE_EXPRESSION}}"
action: "execute {{DIRECTIVE_NAME}}"
```

---

### 2.2 EXECUTIONS Layer
**Purpose**: Pre-built Python tools and workflows, refined via evaluation

**Location**: `{{PROJECT_ROOT}}/executions/`

**Contents**:
```
executions/
├── README.md                           # Index of available tools
├── tools/
│   ├── websocket_implementation.py    # Specialized tool
│   ├── code_analysis.py               # Specialized tool
│   ├── test_execution.py              # Specialized tool
│   └── {{TOOL_NAME}}.py               # Your custom tools
├── workflows/
│   ├── plan.py                        # Planning workflow
│   ├── build.py                       # Build workflow
│   ├── test.py                        # Testing workflow
│   └── {{WORKFLOW_NAME}}.py
├── utils/
│   ├── providers.py                   # LLM provider interface
│   ├── context_manager.py             # Context handling
│   ├── error_handler.py               # Error recovery
│   └── logging_config.py              # Logging setup
└── eval/
    ├── eval_plan.py                   # Evaluate planning outputs
    ├── eval_build.py                  # Evaluate implementation
    └── eval_{{TOOL_NAME}}.py
```

**Execution Tool Pattern (Python)**:
```python
# executions/tools/{{TOOL_NAME}}.py

from typing import Dict, Any, Optional
from executions.utils.context_manager import ContextManager
from executions.utils.error_handler import ErrorHandler

class {{ToolNameCamelCase}}:
    """{{Tool description}}"""
    
    def __init__(self, context: ContextManager):
        self.context = context
        self.error_handler = ErrorHandler()
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool.
        
        Args:
            **kwargs: Tool-specific arguments from directive
        
        Returns:
            Dict with 'path' (file output), 'status', 'data'
        """
        try:
            # Pre-execution: Load context
            self.context.load()
            
            # Execution logic
            result = self._do_work(**kwargs)
            
            # Post-execution: Update context
            self.context.update(result)
            self.context.save()
            
            return {
                'status': 'success',
                'path': result.get('output_path'),
                'data': result
            }
        except Exception as e:
            return self.error_handler.handle(e)
    
    def _do_work(self, **kwargs) -> Dict:
        # Your implementation
        pass
```

**Evaluation Pattern**:
```python
# executions/eval/eval_{{TOOL_NAME}}.py

from typing import Dict, Any
import subprocess
import json

class {{ToolName}}Evaluator:
    """Evaluate {{tool}} outputs against success criteria"""
    
    @staticmethod
    def evaluate(output_path: str) -> Dict[str, Any]:
        """
        Evaluate tool output.
        
        Returns: {'passed': bool, 'metrics': {...}, 'suggestions': [...]}
        """
        # 1. Load output
        # 2. Check success criteria
        # 3. Run automated tests (if applicable)
        # 4. Generate metrics
        # 5. Suggest improvements
        pass
```

---

### 2.3 SHARED KNOWLEDGE BASE Layer
**Purpose**: Cumulative context, expertise, and learning (persistent across sessions)

**Location**: `{{PROJECT_ROOT}}/shared-knowledgebase/`

**Contents**:
```
shared-knowledgebase/
├── README.md                           # Overview
├── expertise/
│   ├── domain_{{DOMAIN}}.md          # Domain knowledge
│   ├── patterns_{{PATTERN}}.md       # Design patterns
│   └── lessons_learned.md            # What we've learned
├── context/
│   ├── identity.md                   # Agent identity & purpose
│   ├── preferences.md                # Agent preferences
│   ├── workflows.md                  # Workflow patterns
│   ├── relationships.md              # Key relationships
│   ├── triggers.md                   # Trigger conditions
│   ├── projects.md                   # Active projects
│   ├── rules.md                      # Behavioral rules
│   ├── session.md                    # Current session state
│   └── journal.md                    # Decision log
└── references/
    ├── architecture.md               # System architecture
    ├── api_contracts.md             # API specifications
    └── troubleshooting.md           # Known issues & solutions
```

**Elle-Inspired 9-Layer Context**:

```yaml
# shared-knowledgebase/context/identity.md
- name: "{{AGENT_NAME}}"
- core_purpose: "{{CORE_PURPOSE}}"
- expertise_areas: ["area1", "area2", "area3"]
- specializations: ["spec1", "spec2"]

# shared-knowledgebase/context/rules.md
rules:
  never:
    - "❌ NEVER execute unvetted code"
    - "❌ NEVER expose API keys"
    - "❌ NEVER modify user files without explicit approval"
  always:
    - "✅ ALWAYS log decisions to journal"
    - "✅ ALWAYS verify source before external requests"
    - "✅ ALWAYS maintain audit trail"

# shared-knowledgebase/context/journal.md
- 2025-12-15T09:30:45Z - [ACTION] Executed plan workflow
  Decision: Route to Anthropic provider for thinking tasks
  Reasoning: Task requires extended reasoning
  Outcome: Generated comprehensive plan
  
- 2025-12-15T10:15:22Z - [LEARNING] Discovered new pattern
  Pattern: KB-first validation prevents hallucination
  Application: Question answering agent
  Update: Added to expertise/patterns_validation.md
```

---

## 3. Planning Mode: State Machine Architecture

The planning mode controls the full execution lifecycle through a robust state machine.

**State Diagram**:
```
STARTUP
  ↓
PROMPT FOR NEW REQUIREMENTS (user provides directives)
  ↓
REFINE REQUIREMENTS (with user/AI feedback)
  ├─→ RECOVERY (Resume interrupted work)
  ├─→ RECOVERY (Mark complete and exit)
  ↓
IMPLEMENT REQUIREMENTS (execute directives → tools → evaluate)
  ├─→ RECOVERY (Resume interrupted work)
  ├─→ RECOVERY (Mark complete and exit)
  ↓
IMPLEMENTATION COMPLETE
  ↓
CLEANUP (archive history, update KB)
```

**Directory Structure** (`{{PROJECT_ROOT}}/planning/`):
```
planning/
├── planner_history.txt              # Audit log (APPEND ONLY)
├── new_requirements.md              # Latest user requirements
├── current_requirements.md          # Active implementation
├── todo.md                          # Task tracking (SHA256 staleness)
├── completed_requirements_*.md      # Historical archive
└── completed_todo_*.md              # Historical archive
```

**Planner History Format**:
```
2025-12-15 14:30:45 - REFINING REQUIREMENTS (new_requirements.md)
2025-12-15 14:30:50 - GIT HEAD (abc1234d)
2025-12-15 14:31:00 - START IMPLEMENTING (current_requirements.md)
                       <<
                       Step 1: Create planning module
                       Step 2: Implement providers
                       Step 3: Add error handling
                       >>
2025-12-15 14:35:12 - COMPLETED REQUIREMENTS (completed_requirements_20251215_143512.md)
2025-12-15 14:35:15 - GIT COMMIT (feat: implement planning module)
```

**CRITICAL INVARIANT**: Write to planner_history BEFORE executing git commit. This invariant must be preserved across all refactoring.

---

## 4. Multi-Provider LLM Support

The framework supports 4 LLM provider types configured in `{{PROJECT_ROOT}}/.env` and code:

```yaml
# {{PROJECT_ROOT}}/.g3.toml or environment config

providers:
  default_provider: "anthropic.default"  # Format: <type>.<name>
  planner: "anthropic.planner"           # Optional role-specific override
  executor: "openai.executor"            # Optional role-specific override
  
  anthropic:
    default:
      api_key: "{{ANTHROPIC_API_KEY}}"
      model: "claude-3-5-sonnet-20241022"
      max_tokens: 64000
    planner:
      api_key: "{{ANTHROPIC_API_KEY}}"
      model: "claude-3-opus-20250219"
      max_tokens: 64000
      thinking_budget_tokens: 16000
  
  openai:
    executor:
      api_key: "{{OPENAI_API_KEY}}"
      model: "gpt-4o"
      max_completion_tokens: 64000
  
  embedded:
    local:
      model: "qwen2.5-7b"  # Auto-downloads if missing
      gpu_enabled: true
```

**Provider Types**:

| Type | Features | Use Case |
|------|----------|----------|
| **Anthropic** | Thinking mode, cache control, 1M context, tool calling | Planning, complex reasoning |
| **OpenAI** | Streaming, tool calling, fast inference | Code generation, real-time tasks |
| **Embedded (llama.cpp)** | Offline, privacy, auto-download Qwen 2.5 7B | Private deployments |
| **Databricks** | OAuth, enterprise auth, token refresh | Enterprise environments |

---

## 5. Autonomous Retry & Error Handling

**Strategy**: Distribute 6 retries over 10 minutes with ±30% jitter

```
Base delays (seconds):  [10,  30,  60,  120, 180, 200] = 600s total
With ±30% jitter:       [7-13, 21-39, 42-78, 84-156, 126-234, 140-260]
```

**Recoverable Errors**: RateLimit (429), NetworkError, ServerError (5xx), ModelBusy, Timeout, TokenLimit, ContextLengthExceeded

**Non-Recoverable Errors**: All other errors → immediate failure with forensic logging

**Forensic Logging** (`{{PROJECT_ROOT}}/logs/errors/`):
```json
{
  "timestamp": "2025-12-15T14:35:12Z",
  "session_id": "sess_20251215_143512",
  "operation": "execute_plan",
  "error": "RateLimit",
  "attempt": 2,
  "retry_delay_ms": 31500,
  "provider": "anthropic",
  "model": "claude-3-5-sonnet",
  "tokens_used": 4250,
  "stack_trace": "..."
}
```

---

## 6. Sequential Task Orchestration (Plan-Build-Improve Pattern)

**Workflow**: Chain tasks with completion gates

```yaml
# directives/workflows/plan_build_improve.yaml

name: "plan_build_improve"
description: "3-step workflow: Create plan → Build implementation → Self-improve"

steps:
  - step: 1
    name: "Create Plan"
    action: "execute_tool"
    tool: "planning"
    inputs:
      user_request: "{{USER_REQUEST}}"
    outputs:
      - name: "path_to_plan"
        from: "result.path"
    gate: "await_completion"  # MUST complete before step 2
    timeout: 600
  
  - step: 2
    name: "Build Implementation"
    action: "execute_tool"
    tool: "build"
    inputs:
      plan_path: "{{PREVIOUS.path_to_plan}}"
    outputs:
      - name: "build_report"
        from: "result.data"
    gate: "await_completion"  # MUST complete before step 3
    timeout: 1200
  
  - step: 3
    name: "Self-Improve Expertise"
    action: "execute_tool"
    tool: "self_improve"
    inputs:
      changes: "{{PREVIOUS.build_report}}"
    outputs:
      - name: "updated_expertise_path"
        from: "result.path"
    gate: "await_completion"
    timeout: 300
  
  - step: 4
    name: "Report Results"
    action: "aggregate_outputs"
    outputs:
      - plan: "{{STEP_1.path_to_plan}}"
      - implementation: "{{STEP_2.build_report}}"
      - updated_expertise: "{{STEP_3.updated_expertise_path}}"
```

**Key Pattern**: Each step uses output from previous step via gate mechanism. NO parallel execution - sequential gates ensure completion.

---

## 7. Rules Engine: ✅ ALWAYS / ❌ NEVER Constraint Enforcement

**Execution Order**: Rules checked FIRST, before any decision logic

```
ACTION REQUESTED
    ↓
[CHECK ❌ NEVER RULES FIRST]
    If any ❌ NEVER rule matches: DENY ACTION
    Else: Continue
    ↓
[CHECK ✅ ALWAYS RULES]
    If any ✅ ALWAYS rule matches: FORCE EXECUTION
    Else: Continue
    ↓
[NORMAL DECISION LOGIC]
    Proceed with standard evaluation
```

**Example Rules** (`shared-knowledgebase/context/rules.md`):
```markdown
# ❌ NEVER Rules (Absolute Denials)
- ❌ NEVER execute unvetted code from untrusted sources
- ❌ NEVER expose API keys or credentials
- ❌ NEVER modify production data without explicit approval
- ❌ NEVER make decisions exceeding cost threshold {{MAX_COST}}

# ✅ ALWAYS Rules (Forced Actions)
- ✅ ALWAYS log decisions with timestamp and reasoning
- ✅ ALWAYS verify source before external API calls
- ✅ ALWAYS maintain audit trail of all modifications
- ✅ ALWAYS update journal with decision outcome
```

---

## 8. Knowledge-First Guardrails (Prevent Hallucination)

**Mandatory Workflow**:

```
QUESTION RECEIVED
    ↓
[STEP 1: CHECK LOCAL KB]
    Search shared-knowledgebase/expertise/
    Is answer already known?
    YES → Return KB answer
    NO → Continue
    ↓
[STEP 2: ASK USER]
    "Question not in KB. May I research online?"
    User denies → Return "Not in KB, external research denied"
    User approves → Continue
    ↓
[STEP 3: INTERNET RESEARCH]
    Execute web search
    Retrieve from reliable sources
    ↓
[STEP 4: UPDATE KB]
    Add findings to shared-knowledgebase/expertise/
    Tag with source URL and date
    ↓
[STEP 5: RETURN ANSWER]
    Answer + "Updated KB: [source]"
```

---

## 9. Session Management & Context Persistence

**Session Lifecycle**:

```
START
  ├─ Load shared-knowledgebase/context/
  ├─ Load shared-knowledgebase/context/session.md
  ├─ Load directives/
  ├─ Load executions/
  │
  ├─ EXECUTE WORKFLOWS
  │  ├─ Update session.md (current task, tokens used)
  │  ├─ Update journal.md (decisions, outcomes)
  │  └─ Execute tools with error recovery
  │
  ├─ PERIODIC SAVES (every N tasks)
  │  ├─ Flush session.md to disk
  │  ├─ Append journal.md entries
  │  └─ Update context/relationships.md if applicable
  │
  ├─ CLEANUP
  │  ├─ Final session save
  │  ├─ Archive planning history
  │  ├─ Update KB with new learning
  │
END
```

**Session File** (`shared-knowledgebase/context/session.md`):
```yaml
session_id: "sess_20251215_143512"
start_time: "2025-12-15T14:35:12Z"
current_workflow: "plan_build_improve"
current_step: 2
tokens_used: 12450
cumulative_tokens: 45200  # From multiple requests
previous_actions:
  - action: "execute_plan"
    timestamp: "2025-12-15T14:35:45Z"
    result: "plan_generated"
active_context:
  user_request: "Implement WebSocket reconnection"
  project: "messaging_system"
  deadline: "2025-12-20"
```

---

## 10. Frontmatter Template for Knowledge Discovery

All expertise and documentation must include frontmatter for hybrid search:

```yaml
---
title: "{{KNOWLEDGE_TITLE}}"
filename: "{{ACTUAL_FILENAME}}.md"
complexity: "beginner|intermediate|expert"
audience: "{{WHO_SHOULD_READ_THIS}}"
category: "{{ORGANIZATIONAL_CATEGORY}}"

# BM25 Keyword Search (12-20 specific terms)
keywords: [keyword1, keyword2, keyword3, ...]

# Vector Semantic Search (4-6 high-level tags)
tags: [tag1, tag2, tag3, tag4]

# 50-80 word comprehensive summary
summary: "{{COMPREHENSIVE_SUMMARY_50_80_WORDS}}"

# Unique anchor phrases for RRF fusion search
rrf_anchors: [anchor1, anchor2, anchor3]

# 120-250 word detailed excerpt showing core value
context_snippet: "{{CONTEXT_SNIPPET_120_250_WORDS}}"
---
```

---

## 11. Project Structure & File Layout

```
{{PROJECT_ROOT}}/
├── directives/                        # Intent & constraints
│   ├── README.md
│   ├── workflows/
│   ├── triggers/
│   ├── constraints/
│   └── agents/
│
├── executions/                        # Pre-built tools & workflows
│   ├── README.md
│   ├── tools/
│   ├── workflows/
│   ├── utils/
│   └── eval/
│
├── shared-knowledgebase/              # Persistent context & expertise
│   ├── README.md
│   ├── expertise/
│   ├── context/
│   └── references/
│
├── planning/                          # Planning state machine files
│   ├── planner_history.txt
│   ├── new_requirements.md
│   ├── current_requirements.md
│   ├── todo.md
│   └── completed_*/
│
├── sessions/                          # Session logs (ephemeral)
│   ├── YYYY-MM-DD/
│   ├── session_id_XXX.log
│   └── session_id_XXX_context.json
│
├── eval/                              # Evaluation results
│   ├── eval_results_{{DATE}}.json
│   └── improvements_{{DATE}}.md
│
├── test/                              # Tests & validation
│   ├── test_directives.py
│   ├── test_executions.py
│   └── test_integration.py
│
├── logs/                              # Audit logs & error forensics
│   ├── errors/
│   ├── audit_{{DATE}}.log
│   └── performance_{{DATE}}.json
│
├── .env                               # Secrets (NOT in git)
├── .env.example                       # Secrets template (IN git)
├── .g3.toml                           # Provider configuration
├── AGENTS.md                          # Agent directory
├── FRAMEWORK.md                       # This file
├── FRAMEWORK-CHECKLIST.md             # Deployment checklist
└── README.md                          # Project overview
```

---

## 12. Agent Directory (AGENTS.md)

```markdown
# Agent Directory

## Planning Agent
- **Role**: Orchestrate planning mode state machine
- **Directives**: `directives/agents/planner_directives.md`
- **Context**: `shared-knowledgebase/context/identity.md`
- **Tools**: plan.py, evaluate_plan.py
- **Triggers**: Manual (user request) or scheduled
- **Rules**: Check `shared-knowledgebase/context/rules.md`

## Execution Agent
- **Role**: Execute tools, handle errors, manage retries
- **Directives**: `directives/agents/executor_directives.md`
- **Tools**: All tools in `executions/tools/`
- **Error Recovery**: 6 retries over 10 minutes
- **Rules**: Check `shared-knowledgebase/context/rules.md`

## Knowledge Agent
- **Role**: Maintain KB, validate expertise, update learning
- **Knowledge Base**: `shared-knowledgebase/`
- **Responsibilities**: Update expertise/, validate against codebase, archive learning
- **Triggers**: After each task completion

## {{CUSTOM_AGENT_NAME}}
- **Role**: {{AGENT_ROLE}}
- **Directives**: `directives/agents/{{agent}}_directives.md`
- **Tools**: {{TOOL_LIST}}
```

---

## 13. Environment Configuration

**File**: `{{PROJECT_ROOT}}/.env` (NEVER commit to git)

```bash
# LLM Provider Configuration
ANTHROPIC_API_KEY="sk-ant-xxx"
OPENAI_API_KEY="sk-xxx"
DATABRICKS_HOST="https://{{DATABRICKS_INSTANCE}}.cloud.databricks.com"
DATABRICKS_TOKEN="dapi-xxx"

# Project Configuration
PROJECT_ROOT="{{PROJECT_ROOT}}"
PROJECT_NAME="{{PROJECT_NAME}}"
AGENT_NAME="{{AGENT_NAME}}"

# Constraints
MAX_COST_PER_REQUEST="0.50"      # USD
MAX_RETRIES="6"
RETRY_TIMEOUT_MINUTES="10"

# Features
ENABLE_THINKING_MODE="true"
ENABLE_FLOCK_MODE="false"       # Default: disabled
ENABLE_KB_FIRST="true"
ENABLE_RULES_CHECKING="true"

# Logging
LOG_LEVEL="INFO"
LOG_TO_FILE="true"
AUDIT_LOG_ENABLED="true"

# External APIs (if KB-first internet research needed)
WEB_SEARCH_ENABLED="false"      # User must approve in workflow
WEB_SEARCH_API_KEY="{{API_KEY}}"
```

**File**: `{{PROJECT_ROOT}}/.env.example` (COMMIT to git)

```bash
# Copy this file to .env and fill in your values
# NEVER commit .env to git

ANTHROPIC_API_KEY="sk-ant-..."
OPENAI_API_KEY="sk-..."
# ... etc
```

---

## 14. Deployment Checklist

See `FRAMEWORK-CHECKLIST.md` for complete preflight verification.

---

## 15. Quick Start

```bash
# 1. Clone/setup
git clone {{REPO_URL}}
cd {{PROJECT_ROOT}}

# 2. Configure
cp .env.example .env
# Edit .env with your API keys

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize structure
python scripts/init_framework.py

# 5. Create first directive
cat > directives/workflows/hello_world.yaml << EOF
name: "hello_world"
steps:
  - step: 1
    action: "log"
    message: "Expert Framework initialized!"
EOF

# 6. Run planning mode
python executions/workflows/plan.py \
  --directive directives/workflows/hello_world.yaml

# 7. Check results
cat planning/planner_history.txt
```

---

## 16. Key Patterns & Best Practices

### Pattern 1: Always Update KB After Learning
```python
# After executing a tool, update expertise
new_knowledge = result['insights']
kb_path = "shared-knowledgebase/expertise/domain_{{DOMAIN}}.md"
append_to_kb(kb_path, new_knowledge, source=result['url'])
```

### Pattern 2: Check Rules FIRST, Always
```python
# Before any decision
if not rules_engine.check_never_rules(action):
    return "Action violates ❌ NEVER rule"

if rules_engine.check_always_rules(action):
    execute(action)  # FORCE IT
    log_to_journal(f"Forced by ✅ ALWAYS rule")
else:
    # Normal decision logic
```

### Pattern 3: Gate Completion Before Next Step
```yaml
- step: 1
  action: "execute_tool"
  gate: "await_completion"  # DON'T SKIP THIS
  timeout: 600
```

### Pattern 4: Log Everything to Journal
```python
journal.append({
    'timestamp': now(),
    'action': action_name,
    'decision': reason,
    'outcome': result,
    'next_steps': []
})
```

---

## 17. Success Criteria

✅ **Deployment Success**:
- [ ] All directives load without syntax errors
- [ ] All tools execute with proper error handling
- [ ] Planning history accurate and APPEND-ONLY
- [ ] Rules engine blocks ❌ NEVER violations
- [ ] KB-first workflow prevents hallucination
- [ ] Session persistence across restarts
- [ ] Retry logic distributes over 10 minutes
- [ ] Journal captures all decisions
- [ ] Expertise updates propagate to KB

✅ **Operational Success**:
- [ ] Autonomous retry succeeds for transient errors
- [ ] Rules checked before every decision
- [ ] Journal auditable for compliance
- [ ] KB grows with each session
- [ ] No manual code changes needed (tools only)

---

## 18. Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "Directive not found" | Typo in directive name | Check `directives/workflows/` for exact name |
| "Tool execution failed" | Missing execution environment | Ensure executions/utils/providers.py configured |
| "KB-first blocked action" | KB validation failed | Approve external research or add to KB |
| "Rule violation" | ❌ NEVER rule matched | Check shared-knowledgebase/context/rules.md |
| "Session lost" | Crash during execution | Check `sessions/` for recovery or `planning/` for state |
| "Infinite retry loop" | Non-recoverable error classified as recoverable | Check error_handler.py classification |

---

## 19. Further Reading

- **G3 Planning Mode Deep Dive**: See synthesis document PHASE-2-SYNTHESIS-G3-REPOSITORY.md
- **Elle Context System**: See synthesis document PHASE-2-SYNTHESIS-ELLE-CONTEXT-SYSTEM.md
- **Reference Frameworks**: See synthesis document PHASE-2-SYNTHESIS-REF-FILES.md
- **Orchestration Patterns**: See synthesis document PHASE-2-SYNTHESIS-ROOT-EXAMPLES.md
- **Knowledge Index**: See COMPREHENSIVE-KNOWLEDGE-INDEX.md

---

**Framework Version**: 1.0  
**Last Updated**: 2025-12-15  
**Status**: Ready for Deployment  
**Next Steps**: Review FRAMEWORK-CHECKLIST.md and deploy
