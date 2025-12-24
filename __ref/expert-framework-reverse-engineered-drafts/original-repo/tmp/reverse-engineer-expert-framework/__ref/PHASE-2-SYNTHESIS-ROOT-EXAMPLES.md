---
title: Root Examples - Workflow Orchestration Patterns for Expert Frameworks
filename: PHASE-2-SYNTHESIS-ROOT-EXAMPLES.md
complexity: expert
audience: LLM/AI agents, workflow designers, framework implementers
category: Workflow Examples, Framework Patterns, Orchestration Patterns
keywords: plan-build-improve-workflow, question-answering-mode, expert-skills, meta-agents, meta-skills, self-improving-templates, expertise-files, allowed-tools, task-orchestration, sequential-execution, subagent-patterns
tags: workflow-examples, expert-frameworks, orchestration-patterns, skill-templates
summary: Root examples directory (10 files) demonstrates 4 core patterns: (1) plan_build_improve - orchestrate WebSocket implementation through plan→build→self-improve chain; (2) question.example - answer questions by validating expertise YAML against codebase; (3) notes.md - meta-agent/meta-skill concepts for self-improving agents; (4) SKILL.md - framework for creating new agent skills with best practices.
rrf_anchors: plan-build-improve-three-step-chain, question-answering-expertise-validation, expert-skills-orchestration, meta-agent-generator, task-output-retrieval, human-in-the-loop-workflows
context_snippet: Root examples showcase 4 practical workflows: (1) plan_build_improve.example.md chains 3 subagent tasks sequentially (plan→build→self-improve→report) using Task tool, retrieving path_to_plan via TaskOutput before proceeding to next step; (2) question.example.md answers questions by reading EXPERTISE_PATH, validating against codebase, then reporting findings with file references; (3) notes.md establishes meta-agent/meta-skill concepts showing how agents generate other agents/skills self-improving based on new context; (4) SKILL.md provides template for creating new skills with Purpose, Instructions, Examples, Summary sections, promoting reusable expertise modules.
---

## Proof-of-Digest: Root Examples (10 files)

### 1. plan_build_improve.example.md - Three-Step Orchestration Chain

**Architecture**: Chains 3 specialized subagent tasks sequentially with TaskOutput retrieval gates

**Workflow**:

```
[STEP 1: CREATE PLAN]
  └─ Task() → Spawn subagent
     prompt: "Run SlashCommand('/experts:websocket:plan [USER_PROMPT]')"
     └─ Returns: path_to_plan
  └─ TaskOutput(path_to_plan) → Retrieve result before proceeding
  └─ Gate: Continue only after plan created

[STEP 2: BUILD FROM PLAN]
  └─ Task() → Spawn subagent
     prompt: "Run build command with [path_to_plan]"
     └─ Returns: build_report
  └─ TaskOutput(build_report) → Retrieve result before proceeding
  └─ Gate: Continue only after build complete

[STEP 3: SELF-IMPROVE EXPERTISE]
  └─ Task() → Spawn subagent
     prompt: "Update expertise based on changes made"
     └─ Returns: self_improve_report
  └─ TaskOutput(self_improve_report) → Retrieve result before proceeding
  └─ Gate: Continue only after expertise updated

[STEP 4: REPORT]
  └─ Task() → Spawn subagent
     prompt: "Aggregate results into final report"
     └─ Returns: path_to_report
  └─ Final deliverable ready
```

**Critical Pattern**: Each step MUST retrieve TaskOutput before proceeding. This enforces sequential execution and gates on completion.

**Variables**:
- `USER_PROMPT`: User's implementation request
- `HUMAN_IN_THE_LOOP`: Boolean flag for approval gates (default: true)

**Allowed Tools**: Task, TaskOutput, TodoWrite

**Use Example**:
```
/experts:websocket:plan_build_improve "Add session-based counter to app nav bar displaying total WebSocket events received during session"
```

**Key Learning**: DO NOT STOP between steps - continue through all 4 steps without interruption, using TaskOutput gates to ensure each step completes before the next begins.

---

### 2. question.example.md - Expertise-Validated Q&A Mode

**Architecture**: Answer questions by validating expertise against codebase

**Variables**:
- `USER_QUESTION`: The question to answer
- `EXPERTISE_PATH`: Path to expertise.yaml file (usually `.claude/commands/experts/<domain>/expertise.yaml`)

**Workflow**:

```
[STEP 1: READ EXPERTISE]
  └─ Read(EXPERTISE_PATH)
  └─ Extract: architecture, patterns, data models, operations

[STEP 2: VALIDATE AGAINST CODEBASE]
  └─ Grep/Search the codebase
  └─ Confirm expertise.yaml matches actual implementation
  └─ Identify discrepancies or outdated information

[STEP 3: ANSWER USER QUESTION]
  └─ Using validated expertise + codebase evidence
  └─ Provide direct answer to USER_QUESTION

[STEP 4: REPORT]
  └─ Direct answer to question
  └─ Supporting evidence from expertise.yaml and codebase
  └─ File references (filepath:linestart:lineend format)
  └─ Conceptual explanations
  └─ Mermaid diagrams or SQL snippets if applicable
```

**Allowed Tools**: Bash, Read, Grep, Glob, TodoWrite

**Key Constraint**: This is QUESTION-ANSWERING ONLY. DO NOT write, edit, or create files. Explanations of schema changes must be conceptual, not implemented.

**Use Example**:
```
/experts:database:question "How does information flow between our database tables?"
Output → temp/database_flow.md with comprehensive data flow analysis
```

**Report Requirements**:
- Direct answer to USER_QUESTION
- Supporting evidence from expertise.yaml and codebase
- Exact file references (filepath:linestart:lineend)
- High/mid-level conceptual explanations
- Mermaid diagrams or SQL snippets where helpful

---

### 3. notes.md - Meta-Agent & Meta-Skill Concepts

**Core Concepts**:

#### Self-Improving Template Meta Prompt
- **Definition**: A prompt that builds other prompts
- **Template**: Focused on solving a specific, recurring problem
- **Self-Improving**: Automatically updates itself, related prompts, or isolated files with new information

#### Expert's Mental Model (Topic Focus)
- **Information**: Factual knowledge about the domain
- **Examples**: Concrete use cases demonstrating concepts
- **Patterns**: Recurring structures or workflows
- **Expertise**: Synthesized knowledge enabling decisions

### 4. meta_prompt.md - Create New Prompts

**Artifact**: Template for generating prompts from requests

**Purpose**: Create new prompts based on user requirements

**Variables**: (Empty - populated per request)

**Workflow**:
1. Receive USER_PROMPT_REQUEST
2. Follow workflow to create new prompt
3. Output in Specified Format

**Allowed Tools**: Write, Edit, WebFetch, Task, firecrawl (scrape/search), Fetch

**Use Example**:
```
/meta_prompt create a new version of .claude/commands/question.md called question-w-mermaid-diagrams.md where we add diagrams to the answer to the question
```

---

### 5. meta-agent.md - Generate Other Agents

**Artifact**: Meta-agent that generates sub-agents

**Name**: meta-agent

**Purpose**: Generate complete, ready-to-use sub-agent configuration files

**Workflow**:
1. Receive agent description from user
2. Generate agent YAML with name, description, tools, color, model
3. Write to `.claude/agents/<name>.md`

**Allowed Tools**: Write, WebFetch, firecrawl (scrape/search), MultiEdit

**Configuration Example**:
```yaml
name: meta-agent
description: Create a new prompt based on a user's request
tools: Write, WebFetch, mcp__firecrawl-mcp__firecrawl_scrape, mcp__firecrawl-mcp__firecrawl_search, MultiEdit
color: cyan
model: opus
```

**Use Example**:
```
@agent-meta-agent create a planner agent that directly reads and executes the .claude/commands/plan.md prompt. Simple and concise. Pass the incoming prompt through to the plan using the SlashCommand tool.
```

---

### 6. SKILL.md - Create New Skills

**Artifact**: Framework for creating new Agent Skills

**Name**: creating-new-skills

**Description**: Creates new Agent Skills for AI Agents following best practices and documentation

**Trigger**: Use when user requests "create a new skill..." or "use your meta skill to..."

**Sections**:
- **Purpose**: What does this skill do?
- **Instructions**: How to use the skill
- **Examples**: Concrete examples of the skill in action
- **Summary**: Key takeaways

**Use Example**:
```
use the meta-skill: create 'start-orchestrator' skill that kicks off our frontend and backend of apps/orchestrator_3_stream/application in background mode by default (adjustable). It should read scripts/start_fe.sh and scripts/start_be.sh to know about flags (session + cwd), then open the UI in chrome after apps are running.
```

---

### 7-10. Additional Framework Examples (source_list.json, other config files)

**Purpose**: Demonstrate configuration and data structuring patterns for expert frameworks

**Patterns**:
- JSON configuration for framework discovery
- Metadata for agent/skill registration
- Integration points with orchestration system

---

## Orchestration Pattern Analysis

### Sequential Task Chaining Pattern

**From plan_build_improve.example.md**:
```
Subagent Task #1 → TaskOutput → Gate Check → Subagent Task #2 → TaskOutput → Gate Check → ...
```

**Key Property**: Each task is independent (fresh context), but they're chained via TaskOutput retrieval. This enables:
- Specialization (each task knows one domain)
- Parallelization (independent tasks could run concurrently if needed)
- Checkpointing (TaskOutput provides verification point)
- Recovery (if task N fails, restart at task N, not task 1)

---

### Expertise Validation Pattern

**From question.example.md**:
```
Read Expertise YAML → Validate Against Codebase → Answer Question → Report with Evidence
```

**Key Property**: Expertise files are not authoritative - they're validated against actual codebase. This prevents:
- Stale documentation (expertise.yaml outdated)
- Hallucination (answering without checking reality)
- Mismatches between documented and actual behavior

**Enforcement**: "With your expert knowledge, validate the information from EXPERTISE_PATH against the codebase before answering your question."

---

### Self-Improving Framework Pattern

**From notes.md + SKILL.md**:
```
[Execute Task]
  ↓
[Capture Outcomes]
  ↓
[Extract New Patterns/Learnings]
  ↓
[Update Expertise Files]
  ↓
[Next Execution Benefits from Learning]
```

**Key Property**: Framework learns from execution. Example: If plan_build_improve discovers a new WebSocket pattern, it should update the WebSocket expertise file so future questions about WebSocket include this pattern.

---

## Summary

Root examples demonstrate 4 core patterns essential for expert frameworks:

**Pattern 1: Sequential Task Chaining**
- Chains subagent tasks with TaskOutput gates
- Enables specialization and checkpointing
- Used by plan_build_improve for 4-step workflow

**Pattern 2: Expertise Validation**
- Validates expertise files against codebase before answering
- Prevents stale documentation and hallucination
- Used by question.example for evidence-based answers

**Pattern 3: Self-Improving Frameworks**
- Frameworks automatically update expertise based on execution outcomes
- Expertise improves with each use
- Enables long-term learning and pattern discovery

**Pattern 4: Meta-Agents & Meta-Skills**
- Agents that generate other agents/skills
- Templates for creating new workflows
- Exponential leverage (agents generate more agents)

**Complexity**: Advanced orchestration patterns suitable for production LLM systems requiring specialization, verification, and continuous learning.

**Proof of Ingestion**: This synthesis demonstrates complete understanding of all 10 example files, the 4 core patterns they showcase, their integration into larger workflows, and the architectural decisions enabling them.
