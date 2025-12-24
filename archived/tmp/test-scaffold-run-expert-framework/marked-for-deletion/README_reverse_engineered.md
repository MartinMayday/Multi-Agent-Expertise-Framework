# Expert Framework - Complete Documentation

## Overview

The Expert Framework is a **Self-Improving Template Meta Prompt** system that enables AI agents to specialize in specific domains, learn from execution, and maintain accurate expertise over time. The framework follows a file-based architecture where experts are organized by domain, each with their own expertise knowledge base.

## Core Concept

**"Self-Improving Template Meta Prompt"**
- **Meta Prompt**: A prompt that builds other prompts
- **Template**: Focused on solving a specific, recurring problem
- **Self-Improving**: Automatically updates itself, related prompts, or isolated files with new information that improves your agent's next execution

## Mental Model: The Expert's Topic Focus

Each expert maintains knowledge in four pillars:

1. **Information** - Factual knowledge about the domain (schemas, APIs, concepts)
2. **Examples** - Concrete use cases demonstrating concepts in practice
3. **Patterns** - Recurring structures, workflows, or solutions that work well
4. **Expertise** - Synthesized knowledge stored in `expertise.yaml` files that enable informed decisions

## Directory Structure

```
.claude/
├── commands/
│   └── experts/
│       ├── database/
│       │   ├── expertise.yaml          # Domain knowledge base
│       │   ├── question.md             # Question-answering mode
│       │   ├── plan.md                 # Planning mode
│       │   ├── build.md                # Building mode
│       │   ├── self-improve.md         # Self-improvement mode
│       │   └── plan_build_improve.md   # Chained workflow
│       ├── websocket/
│       │   ├── expertise.yaml
│       │   ├── question.md
│       │   ├── plan.md
│       │   ├── build.md
│       │   └── self-improve.md
│       └── [other-domains]/
├── agents/
│   ├── planner.md                      # Agent that delegates to /plan
│   ├── meta-agent.md                  # Agent that generates other agents
│   └── [other-agents].md
└── skills/
    ├── creating-new-skills.md          # Meta-skill for creating skills
    └── [other-skills].md
```

## Command Invocation Pattern

Commands are invoked using slash command syntax:

```
/experts:<domain>:<action> [arguments]
```

**Examples:**
- `/experts:database:question "How does information flow between tables?"`
- `/experts:websocket:plan "Add session-based counter"`
- `/experts:websocket:plan_build_improve "Implement WebSocket event tracking"`

## File Types

### 1. Expert Commands (`.claude/commands/experts/<domain>/<action>.md`)

Expert commands are markdown files with YAML frontmatter that define specialized workflows.

**Required Frontmatter:**
```yaml
---
allowed-tools: Bash, Read, Grep, Glob, TodoWrite
description: Brief description of what this command does
argument-hint: [question]  # Optional: hints for expected arguments
---
```

**Required Sections:**
- `# Purpose` - What this command does
- `## Variables` - Named inputs (e.g., `USER_QUESTION: $1`)
- `## Instructions` - Constraints and rules
- `## Workflow` - Step-by-step execution
- `## Report` - Expected output format
- `Use example:` - Usage demonstration

### 2. Expertise Files (`expertise.yaml`)

Expertise files contain the domain's accumulated knowledge in YAML format, structured around the four pillars:

```yaml
information:
  - Factual knowledge about the domain
  - Schemas, APIs, concepts

examples:
  - Concrete use cases
  - Code snippets demonstrating patterns

patterns:
  - Recurring solutions
  - Best practices
  - Common workflows

expertise:
  - Synthesized knowledge
  - Decision-making guidelines
  - Architectural principles
```

**Location:** `.claude/commands/experts/<domain>/expertise.yaml`

### 3. Agents (`.claude/agents/<name>.md`)

Agents are reusable AI assistants that can be invoked with `@agent-<name>`.

**Required Frontmatter:**
```yaml
---
name: agent-name
description: What it does + USE WHEN trigger conditions
tools: Explicit tool allowlist
model: opus  # Optional: model preference
color: cyan  # Optional: UI color
---
```

**Required Sections:**
- `# Purpose` - Single-sentence "why this exists"
- `## Instructions` - How to use the agent
- `## Workflow` - Step-by-step execution
- `## Report` - Expected output format
- `Use example:` - Usage demonstration

### 4. Skills (`.claude/skills/<name>.md`)

Skills are specialized capabilities that agents can use, similar to commands but more focused.

**Required Frontmatter:**
```yaml
---
name: skill-name
description: What it does + USE WHEN trigger conditions
---
```

**Required Sections:**
- `# Purpose` - What this skill does
- `## Instructions` - How to use the skill
- `## Examples` - Concrete examples
- `## Summary` - Key takeaways
- `Use example:` - Usage demonstration

## Core Workflows

### 1. Question-Answering Mode

**Purpose:** Answer questions about a domain without making code changes.

**Pattern:**
1. Read `expertise.yaml` to understand domain architecture
2. Validate expertise against actual codebase
3. Answer question with evidence from both sources
4. Provide file references and conceptual explanations

**Example:** `question.example.md`, `database-expert.example.md`

### 2. Plan-Build-Improve Workflow

**Purpose:** Complete implementation cycle with self-improvement.

**Pattern:**
1. **Plan** - Create structured plan using expertise
2. **Build** - Implement from plan
3. **Self-Improve** - Update expertise based on what was built
4. **Report** - Aggregate results

**Key Constraint:** Each step uses `Task()` to spawn subagents, and `TaskOutput()` to retrieve results before proceeding. **DO NOT STOP between steps.**

**Example:** `plan_build_improve.example.md`

### 3. Self-Improvement Mode

**Purpose:** Validate and update expertise files based on codebase changes.

**Pattern:**
1. Compare `expertise.yaml` against actual codebase
2. Identify discrepancies, missing pieces, or outdated information
3. Update `expertise.yaml` to match reality
4. Ensure expertise remains accurate mental model

**Example:** `self-improve.example.md`

## Best Practices

### ✅ Correct Way to Build Expert Commands

**1. Start with Purpose**
```markdown
# Purpose

Answer questions about database schema, models, and operations without coding.
```

**2. Define Variables Explicitly**
```markdown
## Variables

USER_QUESTION: $1
EXPERTISE_PATH: .claude/commands/experts/database/expertise.yaml
```

**3. Provide Clear Instructions**
```markdown
## Instructions

- IMPORTANT: This is a question-answering task only - DO NOT write, edit, or create any files
- Focus on database schema, Pydantic models, asyncpg operations, and migration patterns
- Validate information from EXPERTISE_PATH against the codebase before answering
```

**4. Define Workflow Steps**
```markdown
## Workflow

- Read the EXPERTISE_PATH file to understand database architecture and patterns
- Review, validate, and confirm information from EXPERTISE_PATH against the codebase
- Respond based on the REPORT section below
```

**5. Specify Report Format**
```markdown
## Report

- Direct answer to the USER_QUESTION
- Supporting evidence from EXPERTISE_PATH and the codebase
- References to the exact files and lines of code that support the answer
- High-mid level conceptual explanations of the data architecture and patterns
```

**6. Include Use Example**
```markdown
Use example:
/experts:database:question [question] e.g how does information flow between our database tables. Write your report to temp/database_flow.md
```

### ❌ Wrong Way to Build Expert Commands

**1. Missing Frontmatter**
```markdown
# Database Expert

Answer questions about databases...
```
**Problem:** No tool restrictions, no description for discovery.

**2. Vague Instructions**
```markdown
## Instructions

- Answer the question
- Use your knowledge
```
**Problem:** No constraints, no validation requirements, no clear boundaries.

**3. No Workflow**
```markdown
## Instructions

Just answer the question about databases.
```
**Problem:** No structured approach, no validation step, no expertise file usage.

**4. Missing Variables**
```markdown
## Instructions

Answer the user's question.
```
**Problem:** Unclear what `$1` refers to, no expertise path defined.

**5. No Report Specification**
```markdown
## Workflow

- Read expertise
- Answer question
```
**Problem:** Unclear output format, no evidence requirements.

**6. No Use Example**
```markdown
## Report

Answer the question.
```
**Problem:** No demonstration of how to invoke the command.

## Expertise File Schema

### Structure

```yaml
# .claude/commands/experts/<domain>/expertise.yaml

information:
  architecture:
    - High-level system design
    - Component relationships
    - Data flow patterns
  
  schemas:
    - Database schemas
    - API contracts
    - Data models
  
  concepts:
    - Key domain concepts
    - Terminology
    - Abstractions

examples:
  code_snippets:
    - title: "Example Title"
      description: "What this demonstrates"
      code: |
        // Example code here
      context: "When to use this pattern"
  
  use_cases:
    - scenario: "Scenario description"
      solution: "How it's solved"
      files: ["path/to/relevant/file.py"]

patterns:
  best_practices:
    - Pattern name: "Description of when and how to use"
  
  anti_patterns:
    - Anti-pattern name: "Why this should be avoided"
  
  workflows:
    - workflow_name: "Step-by-step process"

expertise:
  decision_guidelines:
    - When to use X vs Y
    - Trade-offs to consider
  
  architectural_principles:
    - Core principles for this domain
  
  validation_rules:
    - How to verify correctness
    - What to check before committing
```

### Example: Database Expertise

```yaml
information:
  architecture:
    - "PostgreSQL database with asyncpg for async operations"
    - "Pydantic models for data validation"
    - "Alembic for migrations"
  
  schemas:
    - "users table: id, email, created_at"
    - "sessions table: id, user_id, expires_at"
  
  concepts:
    - "Connection pooling via asyncpg"
    - "Transaction management"

examples:
  code_snippets:
    - title: "Async Database Query"
      description: "How to query database asynchronously"
      code: |
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM users")
      context: "Use for read operations"

patterns:
  best_practices:
    - "Always use connection pooling"
    - "Use transactions for multi-step operations"
  
  anti_patterns:
    - "Don't create new connections per query"
  
  workflows:
    - migration: "1. Create Alembic migration 2. Review SQL 3. Test 4. Apply"

expertise:
  decision_guidelines:
    - "Use asyncpg for async, psycopg2 for sync"
    - "Pydantic for validation, SQLAlchemy for ORM needs"
  
  architectural_principles:
    - "Database is source of truth"
    - "Models mirror schema exactly"
  
  validation_rules:
    - "Check migrations are reversible"
    - "Verify indexes on foreign keys"
```

## Agent Patterns

### Meta-Agent Pattern

Agents that generate other agents or commands.

**Example:** `meta-agent.md`
- Takes user description of new agent
- Generates complete agent configuration
- Writes to `.claude/agents/<name>.md`

### Delegation Pattern

Agents that delegate to commands.

**Example:** `planner.example.md`
- Receives user prompt
- Executes `/plan [user prompt]` via SlashCommand
- Returns plan output

### Skill Pattern

Reusable capabilities that follow skill template.

**Example:** `start-orchestrator_skill.md`
- Defines specific capability
- Includes prerequisites, configuration, workflow
- Provides examples

## Self-Improvement Mechanism

The framework's key innovation is self-improvement:

1. **Execution** - Agent executes task using expertise
2. **Validation** - Agent compares expertise against actual codebase
3. **Update** - Agent updates expertise.yaml with new learnings
4. **Next Execution** - Future executions benefit from updated expertise

**Critical Rule:** Always validate expertise against codebase before trusting it. Expertise files are not authoritative - the codebase is.

## Chaining Commands

Commands can be chained into workflows:

**Example:** `plan_build_improve.md`
- Chains: plan → build → self-improve → report
- Uses `Task()` to spawn subagents
- Uses `TaskOutput()` to retrieve results
- **Critical:** DO NOT STOP between steps

**Pattern:**
```markdown
### Step 1: Create Plan
Task(
    subagent_type: "general-purpose",
    prompt: "Run SlashCommand('/experts:websocket:plan [USER_PROMPT]'). Return the path to the generated plan file."
)
TaskOutput(path_to_plan) → Retrieve before proceeding

### Step 2: Build
Task(
    subagent_type: "general-purpose",
    prompt: "Run SlashCommand('/experts:websocket:build [path_to_plan]'). Return build report."
)
TaskOutput(build_report) → Retrieve before proceeding
```

## Integration with Claude Desktop

### Slash Commands

Commands are invoked via slash command syntax:
- `/experts:database:question [question]`
- `/experts:websocket:plan [request]`
- `/experts:websocket:plan_build_improve [request]`

### Agent Invocation

Agents are invoked with `@agent-<name>`:
- `@agent-planner create a plan for feature X`
- `@agent-meta-agent create a database expert agent`

### Skill Usage

Skills are referenced in agent descriptions:
- "USE WHEN the user wants to start the orchestrator"
- "USE WHEN the user asks to create a new skill"

## Validation Checklist

Before deploying an expert command, verify:

- [ ] Frontmatter includes `allowed-tools` and `description`
- [ ] Purpose section clearly defines what the command does
- [ ] Variables section names all inputs (e.g., `USER_QUESTION: $1`)
- [ ] Instructions section includes constraints and validation rules
- [ ] Workflow section provides step-by-step execution
- [ ] Report section specifies expected output format
- [ ] Use example demonstrates invocation syntax
- [ ] Expertise file exists at `.claude/commands/experts/<domain>/expertise.yaml`
- [ ] Expertise file follows four-pillar structure (Information, Examples, Patterns, Expertise)

## Common Patterns

### Question-Answering Pattern
- Read-only operations
- Validate expertise against codebase
- Provide evidence and file references
- Include diagrams where helpful

### Planning Pattern
- Read expertise to understand domain
- Create structured plan
- Reference existing patterns
- Output to file for review

### Building Pattern
- Read plan file
- Implement following expertise patterns
- Validate against expertise
- Create/update code files

### Self-Improvement Pattern
- Compare expertise.yaml to codebase
- Identify discrepancies
- Update expertise.yaml
- Ensure accuracy for next execution

## Troubleshooting

### Expertise File Outdated
**Symptom:** Answers don't match actual codebase
**Solution:** Run self-improve command to update expertise

### Command Not Found
**Symptom:** `/experts:domain:action` not recognized
**Solution:** Verify file exists at `.claude/commands/experts/<domain>/<action>.md` with correct frontmatter

### Subagent Fails
**Symptom:** Task() spawns subagent but it fails
**Solution:** Ensure subagent prompt includes complete context (subagents start fresh)

### Expertise Validation Fails
**Symptom:** Expertise doesn't match codebase
**Solution:** This is expected - run self-improve to update expertise file

## Next Steps

1. **Create Your First Expert**
   - Choose a domain (e.g., `frontend`, `api`, `testing`)
   - Create directory: `.claude/commands/experts/<domain>/`
   - Create `expertise.yaml` with four-pillar structure
   - Create `question.md` command
   - Test with `/experts:<domain>:question "test question"`

2. **Add Planning Capability**
   - Create `plan.md` command
   - Reference expertise in planning workflow
   - Test with `/experts:<domain>:plan "plan request"`

3. **Add Building Capability**
   - Create `build.md` command
   - Implement from plans
   - Test with `/experts:<domain>:build [plan_file]`

4. **Enable Self-Improvement**
   - Create `self-improve.md` command
   - Validate and update expertise
   - Test after making code changes

5. **Chain Workflows**
   - Create `plan_build_improve.md`
   - Chain plan → build → self-improve
   - Test complete workflow

## References

- Source Video: https://www.youtube.com/watch?v=zTcDwqopvKE
- Framework Concept: "Self-Improving Template Meta Prompt"
- Mental Model: Information, Examples, Patterns, Expertise

