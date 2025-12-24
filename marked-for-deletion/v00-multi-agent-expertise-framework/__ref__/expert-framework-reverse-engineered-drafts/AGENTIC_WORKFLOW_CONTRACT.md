# AGENTIC WORKFLOW CONTRACT v1.0

**System Architecture**: File-based agentic workflow for IDE-agnostic, multi-model orchestration  
**Philosophy**: Filesystem-as-API, AI-as-orchestrator, documentation-first execution  
**Enforcement**: MetaGPT validates all agent behaviors against this contract

---

## Contract Principles

1. **Explicit Over Implicit** - All permissions, ownership, and behaviors are declared
2. **Read-Only by Default** - Agents cannot write unless explicitly granted permission
3. **Single Responsibility** - Each path serves one clear purpose
4. **Isolation First** - Agent state never leaks between agents without handoff
5. **Evidence Required** - All responses must trace to documentation, KB, or execution results

---

## Root Structure

```
<project-root>/
├── agents/                    # Agent definitions (one folder per agent)
├── shared-knowledgebase/      # Cross-agent knowledge repository
├── directives/                # Global behavior contracts
├── sessions/                  # Session state and history
├── review-approval/           # Staging area for human-reviewed changes
├── staging/                   # Staging area for machine outputs
└── AGENTIC_WORKFLOW_CONTRACT.md  # This file
```

---

## 1. `agents/<agentname>/` - Agent Definition Container

### Purpose
Self-contained agent specification with instructions, knowledge, tools, tests, and execution history.

### Structure
```
agents/<agentname>/
├── <agentname>_system-instructions.md  # Agent behavior specification
├── kb_<agentname>-manifest.md          # Agent-specific knowledge index
├── AGENTS.md                            # Agent catalog awareness
├── directives/                          # Agent-specific behavior rules
├── executions/                          # Python tools and workflows
├── test/                                # Agent validation tests
├── eval/                                # Maturity scoring and metrics
├── sessions/                            # Agent execution history
├── mcp.json                             # MCP-server tool configuration
└── .env                                 # Model selection and secrets
```

### Read Access
- **Agent itself**: Full read access to own folder
- **MetaGPT**: Full read access to all agent folders (orchestration)
- **Other agents**: Read-only access to `AGENTS.md` and `kb_*-manifest.md` (discovery only)

### Write Access
- **Agent itself**: Can write to `sessions/`, `eval/`, and propose updates to `kb_*-manifest.md`
- **MetaGPT**: Can write to any file when creating/updating agents
- **System**: Can write to `test/` and `eval/` based on automated validation

### Owned By
Agent-specific, orchestrated by MetaGPT

### Forbidden Actions
- ❌ Agents cannot modify another agent's `system-instructions.md`
- ❌ Agents cannot execute another agent's `executions/` directly
- ❌ Agents cannot read another agent's `sessions/` (privacy boundary)
- ❌ Agents cannot modify their own `system-instructions.md` (use MetaGPT to request changes)

---

## 2. `<agentname>_system-instructions.md` - Agent Behavior Specification

### Purpose
Complete agent definition following expert framework pattern with frontmatter-driven behavior.

### Required Structure
```markdown
---
name: agent-name
description: What it does + USE WHEN automatic invocation triggers
tools: [Tool1, Tool2, Tool3]  # Explicit allowlist
model: claude-sonnet-4.5  # Default model (override via .env)
complexity: beginner|intermediate|advanced
argument-hint: [expected_input_format]
allowed-tools: Bash, Read, Write, WebSearch, etc.
---

# Purpose
Single-sentence agent mission statement.

## Variables
Named input parameters (e.g., USER_QUESTION: $1)

## Instructions
- Constraints and behavioral rules
- Must include: "READ directives/KB_GUARDRAILS.md and follow strictly"
- Model-specific optimizations if needed

## Workflow
1. Step-by-step execution process
2. Explicit handoff points
3. Failure handling procedures

## Report
Expected output format and structure

## Examples
Usage demonstrations with input/output pairs
```

### Read Access
- **Agent itself**: Always loaded on invocation
- **MetaGPT**: Reads to understand agent capabilities
- **Other agents**: Can read via `AGENTS.md` catalog reference

### Write Access
- **MetaGPT only**: Updates agent definitions based on user requests or self-improvement feedback

### Owned By
MetaGPT (agents request changes, don't modify directly)

### Forbidden Actions
- ❌ Self-modification during execution
- ❌ Overriding KB-first guardrails
- ❌ Skipping workflow steps

---

## 3. `kb_<agentname>-manifest.md` - Agent-Specific Knowledge Index

### Purpose
Agent-local knowledge base index with progressive loading metadata. Links to detailed knowledge snippets.

### Required Structure
```markdown
---
agent: agentname
kb_type: agent-specific
last_updated: YYYY-MM-DD
total_snippets: N
---

# Agent Knowledge Manifest

## Quick Reference (Always Loaded)
Brief one-line descriptions of available knowledge areas.

## Knowledge Snippets (Load on Demand)
- [snippet-id](../shared-knowledgebase/snippets/<topic>.md) - brief description
- [snippet-id](kb_local/<topic>.md) - agent-specific knowledge

## External References
- Official docs: <url>
- Related agents: <agentname>
```

### Read Access
- **Agent itself**: Reads manifest always, loads snippets on-demand
- **MetaGPT**: Reads for orchestration decisions
- **Other agents**: Read-only for discovery

### Write Access
- **Agent**: Can propose additions via handoff to MetaGPT
- **MetaGPT**: Approves and writes updates
- **Self-improve agents**: Update after validation against codebase

### Owned By
Agent-specific, coordinated by MetaGPT

### Forbidden Actions
- ❌ Direct modification during task execution
- ❌ Loading all snippets upfront (violates progressive loading)
- ❌ Removing snippets without archival

---

## 4. `AGENTS.md` - Agent Catalog

### Purpose
Agent discovery and capability advertisement. Enables agents to request delegation or find specialists.

### Required Structure
```markdown
# Agent Catalog

## MetaGPT (Orchestrator)
- **Role**: Prompt decomposition and workflow coordination
- **Invocation**: Automatic on braindump prompts
- **Model**: claude-sonnet-4.5

## ResearchGPT
- **Role**: Documentation-first research
- **Triggers**: "research", "find documentation", "gather info"
- **Tools**: web.search, web.scrape, web.fetch
- **Model**: claude-sonnet-4.5

[... other agents ...]

## Request New Agent
If no existing agent fits your needs, return to MetaGPT with:
- Required capabilities
- Expected inputs/outputs
- Suggested name
```

### Read Access
- **All agents**: Read-only access for discovery
- **MetaGPT**: Reads for orchestration

### Write Access
- **MetaGPT only**: Updates when agents are added/modified

### Owned By
System (managed by MetaGPT)

### Forbidden Actions
- ❌ Agents cannot add themselves to catalog
- ❌ Agents cannot modify other agent descriptions

---

## 5. `directives/` - Behavior Contracts

### Purpose
Reusable, enforceable behavior rules that agents must follow. Drop-in modules for system prompts.

### Standard Directives
```
directives/
├── KB_GUARDRAILS.md           # Mandatory KB-first execution protocol
├── HANDOFF_PROTOCOL.md        # State transfer requirements
├── PROGRESSIVE_LOADING.md     # Context management rules
├── FAILURE_HANDLING.md        # How to fail gracefully
├── OUTPUT_CONTRACTS.md        # Response format standards
└── <agentname>/               # Agent-specific overrides
    └── custom-directive.md
```

### Read Access
- **All agents**: MUST read applicable directives before execution
- **MetaGPT**: Enforces directive compliance

### Write Access
- **MetaGPT only**: Creates and updates directives
- **Agents**: Cannot modify (request changes via handoff)

### Owned By
System (immutable contracts)

### Forbidden Actions
- ❌ Ignoring or skipping directive instructions
- ❌ Implementing conflicting behaviors
- ❌ Self-modification of directives

---

## 6. `executions/` - Python Tools and Workflows

### Purpose
Deterministic Python scripts that handle computation, file operations, and complex logic outside LLM context.

### Structure
```
executions/
├── tools/                  # Single-purpose utilities
│   ├── parse_manifest.py
│   ├── validate_kb.py
│   └── search_hybrid.py
├── workflows/              # Multi-step processes
│   ├── research_pipeline.py
│   └── eval_maturity.py
└── README.md               # Execution catalog
```

### Read Access
- **Agent itself**: Reads to understand available tools
- **MetaGPT**: Reads for orchestration
- **Execution engine**: Executes scripts

### Write Access
- **Agents**: Can REQUEST new tools via handoff (describe needed capability)
- **MetaGPT**: Creates new tools based on agent requests
- **Self-improve agents**: Update existing tools after validation

### Owned By
Agent-specific, validated by test/

### Forbidden Actions
- ❌ Agents cannot execute arbitrary Python code
- ❌ Agents cannot modify executions/ without testing
- ❌ Tools cannot access other agents' sessions/

---

## 7. `test/` - Agent Validation

### Purpose
Automated tests that validate agent behavior, tool correctness, and KB accuracy.

### Structure
```
test/
├── unit/                   # Individual component tests
├── integration/            # Agent workflow tests
├── fixtures/               # Test data
└── test_results/           # Latest test outputs
```

### Read Access
- **Agent**: Reads test results to understand failures
- **MetaGPT**: Reads to validate agent readiness
- **Eval system**: Reads to compute maturity scores

### Write Access
- **Test runner**: Writes test results
- **Agents**: Can propose new tests via handoff

### Owned By
System (automated validation)

### Forbidden Actions
- ❌ Agents cannot skip failing tests
- ❌ Agents cannot modify tests to make them pass
- ❌ Disabling tests without documentation

---

## 8. `eval/` - Maturity Scoring

### Purpose
Track agent performance, reliability, and knowledge completeness over time.

### Structure
```
eval/
├── metrics/                # Performance measurements
├── maturity_score.json     # Current agent maturity rating
├── improvement_log.md      # History of enhancements
└── failure_analysis.md     # Post-mortem on errors
```

### Read Access
- **Agent**: Reads to understand performance gaps
- **MetaGPT**: Reads for orchestration decisions (route to mature agents)
- **Self-improve agents**: Reads to prioritize improvements

### Write Access
- **Eval hooks**: Automatic writes after each execution
- **Self-improve agents**: Update improvement_log.md

### Owned By
System (automated scoring)

### Forbidden Actions
- ❌ Manually inflating maturity scores
- ❌ Deleting failure analysis without resolution

---

## 9. `sessions/` - Execution History

### Purpose
Persistent record of agent executions for continuity, debugging, and learning.

### Structure
```
sessions/
├── YYYY-MM-DD/
│   ├── session-<uuid>.json     # Full execution trace
│   ├── inputs.md               # What the agent received
│   ├── outputs.md              # What the agent produced
│   └── kb_updates.md           # KB modifications proposed
└── active_session.json         # Current running session
```

### Read Access
- **Agent itself**: Reads own session history for continuity
- **MetaGPT**: Reads for debugging and handoff context
- **Self-improve agents**: Reads to identify patterns

### Write Access
- **Agent**: Appends to session logs during execution
- **System**: Creates new session files on invocation

### Owned By
Agent-specific (privacy boundary)

### Forbidden Actions
- ❌ Reading other agents' sessions
- ❌ Modifying historical session data
- ❌ Deleting sessions without archival

---

## 10. `mcp.json` - MCP-Server Configuration

### Purpose
Declares available MCP-server tools and their capabilities.

### Required Structure
```json
{
  "agent": "agentname",
  "model": "claude-sonnet-4.5",
  "mcp_servers": {
    "web.search": {
      "required": true,
      "priority": "high",
      "fallback": "manual_search"
    },
    "web.scrape": {
      "required": false,
      "priority": "medium"
    }
  }
}
```

### Read Access
- **Agent**: Reads to understand available tools
- **MetaGPT**: Reads for capability assessment

### Write Access
- **Agent**: Can REQUEST new tools via handoff
- **MetaGPT**: Updates tool declarations

### Owned By
Agent-specific

### Forbidden Actions
- ❌ Assuming tool availability without checking
- ❌ Executing tools not declared in mcp.json

---

## 11. `.env` - Model Selection and Secrets

### Purpose
Agent-specific configuration for model selection and API credentials.

### Required Variables
```bash
# Model Configuration
AGENT_MODEL=claude-sonnet-4.5
AGENT_FALLBACK_MODEL=claude-haiku-4.5
MODEL_PROVIDER=anthropic

# Multi-Model Options
OPENAI_MODEL=gpt-5.2
GOOGLE_MODEL=gemini-pro-3.0
MOONSHOT_MODEL=kimi-k2

# MCP Configuration
MCP_TIMEOUT=30
MCP_RETRY_COUNT=3
```

### Read Access
- **Agent**: Reads to determine model selection
- **Execution engine**: Reads for API configuration

### Write Access
- **User/MetaGPT**: Updates model preferences
- **Agents**: Cannot modify (request via handoff)

### Owned By
User/System

### Forbidden Actions
- ❌ Hardcoding model selection in system-instructions
- ❌ Exposing secrets in logs or outputs
- ❌ Overriding model selection without .env update

---

## 12. `shared-knowledgebase/` - Cross-Agent Knowledge

### Purpose
Centralized repository of verified knowledge accessible to all agents via progressive loading.

### Structure
```
shared-knowledgebase/
├── manifest.md                 # Master index
├── snippets/                   # Individual knowledge units
│   ├── <topic>.md
│   └── <category>/
│       └── <specific>.md
├── frameworks/                 # Reusable methodologies
│   ├── first-principles-thinking.md
│   └── kb-snippet-format.md
└── archives/                   # Deprecated knowledge
```

### Read Access
- **All agents**: Progressive loading via manifest
- **MetaGPT**: Full access for orchestration

### Write Access
- **Agents**: Propose additions via handoff
- **MetaGPT**: Approves and writes updates
- **Self-improve agents**: Update after validation

### Owned By
System (collective knowledge)

### Forbidden Actions
- ❌ Loading entire knowledgebase into context
- ❌ Modifying snippets without source validation
- ❌ Creating duplicate snippets (check manifest first)

---

## 13. `shared-knowledgebase/manifest.md` - Master Knowledge Index

### Purpose
Progressive loading gateway with optimized retrieval metadata for all agents.

### Required Structure
```markdown
---
index_type: master-knowledge-catalog
total_snippets: N
last_updated: YYYY-MM-DD
retrieval_strategy: hybrid (BM25 + semantic + RRF)
---

# Knowledge Base Manifest

## Quick Reference (Always Loaded - L1)
One-line descriptions of knowledge areas.

## Knowledge Categories (L2 - Load on Request)
### Architecture Patterns
- [snippet-id](snippets/architecture/pattern-name.md) - brief

### Agent Frameworks
- [snippet-id](snippets/frameworks/framework-name.md) - brief

## Retrieval Optimization
**BM25 Keywords**: [keyword list for lexical search]
**Semantic Anchors**: [concept list for embeddings]
**RRF Bridges**: [terminology mappings]
```

### Read Access
- **All agents**: MUST read before claiming "no knowledge available"
- **MetaGPT**: Full access for orchestration

### Write Access
- **MetaGPT only**: Updates index when snippets added/removed

### Owned By
System

### Forbidden Actions
- ❌ Bypassing manifest and searching snippets directly
- ❌ Loading all L2 content without need assessment

---

## 14. `sessions/` (Global) - Cross-Agent Coordination

### Purpose
Inter-agent communication and workflow state management.

### Structure
```
sessions/
├── workflows/
│   └── <workflow-id>/
│       ├── state.json          # Current workflow state
│       ├── handoffs.log        # Agent-to-agent transfers
│       └── artifacts/          # Produced outputs
└── active_workflows.json       # Currently running workflows
```

### Read Access
- **MetaGPT**: Full access for orchestration
- **Active agents**: Read own workflow state
- **Evaluation agents**: Read for post-mortem

### Write Access
- **MetaGPT**: Creates workflows and manages state
- **Agents**: Append to handoffs.log

### Owned By
MetaGPT (orchestrator)

### Forbidden Actions
- ❌ Agents modifying workflow state directly
- ❌ Bypassing handoff protocol
- ❌ Reading workflows they're not participating in

---

## 15. `review-approval/` - Human-Reviewed Change Staging

### Purpose
Staging area for all new or modified files that require human review, validation, and approval before promotion to canonical locations.

### Structure
```
review-approval/
├── README.md              # Staging workflow documentation
├── changeset.yaml        # Change manifest (what, why, target paths)
└── patches/              # Optional diffs or patch files
```

### Read Access
- **All agents**: Full read access to review staged changes
- **MetaGPT**: Full read access for orchestration

### Write Access
- **All agents**: Can write new/changed files here (default write location)
- **MetaGPT**: Can write changesets and promotion logs

### Promotion Gate
Files can only be promoted to canonical locations after:
- ✅ Validation passes (`validate_scaffold.py`)
- ✅ Tests pass (if applicable)
- ✅ Human approval granted
- ✅ Promotion checklist completed

### Forbidden Actions
- ❌ Direct writes to canonical locations without staging
- ❌ Promotion without validation
- ❌ Promotion without approval
- ❌ Skipping changeset creation

---

## 16. `staging/` - Machine Output Staging

### Purpose
Staging area for machine-generated outputs from execution tools, workflows, and automated processes. Unlike `review-approval/`, this area is for intermediate outputs that may not need human review.

### Structure
```
staging/
├── README.md              # Staging documentation
└── out/                  # Tool outputs, generated files, logs
    ├── generated/        # Generated artifacts
    ├── logs/            # Execution logs
    └── temp/            # Temporary files
```

### Read Access
- **All agents**: Full read access to use staged outputs
- **MetaGPT**: Full read access for orchestration

### Write Access
- **Execution tools**: Can write outputs here
- **Workflows**: Can stage intermediate results here
- **Eval/metrics**: Can write results here

### Promotion
Files in `staging/out/` can be:
- Used directly by other tools (no promotion needed)
- Promoted to canonical locations via `review-approval/` workflow if they become permanent artifacts
- Cleaned up automatically after workflow completion

### Forbidden Actions
- ❌ Writing secrets or sensitive data (even to staging)
- ❌ Using staging as permanent storage (promote or clean up)

---

## Enforcement Rules (MetaGPT Authority)

### MetaGPT MUST Reject:
1. Agent outputs that skip KB-first checks
2. Direct writes to canonical locations without staging (except with explicit user permission)
3. Promotion requests without validation or approval
2. Handoffs without proper state contracts
3. File modifications outside write permissions
4. Tool usage not declared in mcp.json
5. Responses without source traceability

### MetaGPT MUST Enforce:
1. All directives are followed
2. Progressive loading is used (no context bloat)
3. Failure is handled gracefully
4. KB updates are proposed after research
5. Sessions are logged for continuity

### MetaGPT Authority Hierarchy:
```
AGENTIC_WORKFLOW_CONTRACT.md  (highest - immutable)
  ↓
directives/KB_GUARDRAILS.md    (enforced for all agents)
  ↓
directives/HANDOFF_PROTOCOL.md (enforced for transitions)
  ↓
<agentname>_system-instructions.md (agent-specific)
```

---

## Validation Checklist (Before Agent Execution)

Every agent invocation must pass:

- [ ] Agent has valid `system-instructions.md` with frontmatter
- [ ] Agent has read applicable `directives/`
- [ ] Agent has checked `kb_<agent>-manifest.md` (KB-first gate)
- [ ] Agent has declared KB sufficiency status
- [ ] If research needed: user approved and sources tracked
- [ ] Tools used are declared in `mcp.json`
- [ ] Model selection follows `.env` configuration
- [ ] Session logging is enabled
- [ ] Handoff contract prepared (if transitioning)

---

## Contract Versioning

**Current Version**: 1.0  
**Last Updated**: 2025-12-22  
**Breaking Changes**: None yet (initial version)

### Version Update Process:
1. Propose changes via issue/discussion
2. Validate against existing agent behaviors
3. Update all affected agent instructions
4. Increment version number
5. Document breaking changes

---

## Quick Reference: Permission Matrix

| Path | Agent Read | Agent Write | MetaGPT Read | MetaGPT Write | Other Agent Read |
|------|-----------|------------|--------------|---------------|------------------|
| `<agent>_system-instructions.md` | ✅ Own | ❌ | ✅ All | ✅ All | ✅ Via catalog |
| `kb_<agent>-manifest.md` | ✅ Own | 🟡 Propose | ✅ All | ✅ All | ✅ Discovery |
| `AGENTS.md` | ✅ All | ❌ | ✅ | ✅ | ✅ |
| `directives/` | ✅ Required | ❌ | ✅ | ✅ | ✅ |
| `executions/` | ✅ Own | 🟡 Request | ✅ All | ✅ All | ❌ |
| `test/` | ✅ Results | 🟡 Propose | ✅ | ✅ | ❌ |
| `eval/` | ✅ Own | 🟡 Append | ✅ All | ✅ All | ❌ |
| `sessions/` (own) | ✅ Own | ✅ Append | ✅ All | ✅ All | ❌ |
| `sessions/` (other) | ❌ | ❌ | ✅ All | ✅ All | ❌ |
| `mcp.json` | ✅ Own | 🟡 Request | ✅ All | ✅ All | ❌ |
| `.env` | ✅ Own | ❌ | ✅ All | ✅ All | ❌ |
| `shared-knowledgebase/manifest.md` | ✅ All | 🟡 Propose | ✅ | ✅ | ✅ |
| `shared-knowledgebase/snippets/` | ✅ On-demand | 🟡 Propose | ✅ | ✅ | ✅ On-demand |

**Legend**:  
✅ = Allowed  
❌ = Forbidden  
🟡 = Propose to MetaGPT, cannot modify directly

---

## Philosophy Summary

This contract establishes:
- **Deterministic Behavior**: Agents follow documented contracts, not assumptions
- **Progressive Disclosure**: Context loads only when needed
- **Fail-Safe Defaults**: Read-only unless explicitly granted write permission
- **Auditability**: All actions trace to contracts, KB, or executions
- **Composability**: Agents combine through well-defined interfaces

**Core Insight**: By treating the filesystem as an API with explicit contracts, we eliminate the ambiguity that causes agent drift, hallucinations, and unpredictable behavior.

---

*This contract is the foundation. All agents, directives, and workflows must comply.*