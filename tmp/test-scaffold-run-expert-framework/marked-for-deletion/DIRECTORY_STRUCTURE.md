# Expert Framework - Directory Structure

Complete directory structure for the Expert Framework with explanations and examples.

## Root Structure

```
.claude/
├── commands/
│   └── experts/
│       ├── <domain>/
│       │   ├── expertise.yaml          # Domain knowledge base
│       │   ├── question.md             # Question-answering mode
│       │   ├── plan.md                 # Planning mode
│       │   ├── build.md                # Building mode
│       │   ├── self-improve.md         # Self-improvement mode
│       │   └── plan_build_improve.md   # Chained workflow (optional)
│       └── [other-domains]/
├── agents/
│   ├── planner.md                      # Example: Delegation agent
│   ├── meta-agent.md                   # Example: Meta-agent
│   ├── database-expert.md             # Example: Domain expert agent
│   └── [other-agents].md
└── skills/
    ├── creating-new-skills.md          # Meta-skill example
    └── [other-skills].md
```

## Directory Descriptions

### `.claude/commands/experts/`

**Purpose:** Contains expert commands organized by domain.

**Structure:**
- Each domain has its own subdirectory
- Domain name should be lowercase, descriptive (e.g., `database`, `websocket`, `frontend`)
- Each domain contains:
  - `expertise.yaml` - Required: Domain knowledge base
  - `question.md` - Optional: Question-answering command
  - `plan.md` - Optional: Planning command
  - `build.md` - Optional: Building command
  - `self-improve.md` - Optional: Self-improvement command
  - `plan_build_improve.md` - Optional: Chained workflow

**Example Domains:**
- `database/` - Database schema, models, queries
- `websocket/` - WebSocket implementation patterns
- `frontend/` - Frontend components, UI patterns
- `api/` - API design, endpoints, contracts
- `testing/` - Testing strategies, patterns

### `.claude/agents/`

**Purpose:** Contains reusable AI agent configurations.

**Structure:**
- Each agent is a single `.md` file
- File name matches agent name (e.g., `planner.md` → `@agent-planner`)
- Agents can delegate to commands or perform specialized workflows

**Common Agent Types:**
- **Delegation Agents**: Simple wrappers that delegate to commands
- **Meta-Agents**: Agents that generate other agents/commands
- **Domain Expert Agents**: Specialized agents for specific domains
- **Orchestration Agents**: Agents that chain multiple commands

### `.claude/skills/`

**Purpose:** Contains specialized capabilities that agents can use.

**Structure:**
- Each skill is a single `.md` file
- Skills are more focused than agents
- Referenced in agent descriptions with "USE WHEN" triggers

**Example Skills:**
- `creating-new-skills.md` - Meta-skill for creating skills
- `start-orchestrator.md` - Skill for starting services
- `code-review.md` - Skill for reviewing code

## File Naming Conventions

### Expert Commands
- Use lowercase with hyphens: `question.md`, `plan.md`, `build.md`
- Descriptive names that match their function
- Standard names: `question`, `plan`, `build`, `self-improve`, `plan_build_improve`

### Agents
- Use lowercase with hyphens: `planner.md`, `meta-agent.md`
- File name becomes agent invocation: `planner.md` → `@agent-planner`
- Descriptive names that indicate agent purpose

### Skills
- Use lowercase with hyphens: `creating-new-skills.md`
- Descriptive names that indicate skill capability
- Referenced in agent descriptions, not directly invoked

## Example Directory Structure

### Complete Example: Database Expert

```
.claude/
├── commands/
│   └── experts/
│       └── database/
│           ├── expertise.yaml
│           ├── question.md
│           ├── plan.md
│           ├── build.md
│           ├── self-improve.md
│           └── plan_build_improve.md
├── agents/
│   └── database-expert.md
└── skills/
    └── [no database-specific skills]
```

**Invocation Examples:**
- `/experts:database:question "How does our schema work?"`
- `/experts:database:plan "Add user preferences table"`
- `/experts:database:plan_build_improve "Implement audit logging"`
- `@agent-database-expert How does information flow between tables?`

### Complete Example: WebSocket Expert

```
.claude/
├── commands/
│   └── experts/
│       └── websocket/
│           ├── expertise.yaml
│           ├── question.md
│           ├── plan.md
│           ├── build.md
│           ├── self-improve.md
│           └── plan_build_improve.md
├── agents/
│   └── websocket-expert.md
└── skills/
    └── [no websocket-specific skills]
```

**Invocation Examples:**
- `/experts:websocket:question "How do we handle reconnection?"`
- `/experts:websocket:plan "Add session-based event counter"`
- `/experts:websocket:plan_build_improve "Implement real-time notifications"`

## File Locations Reference

### Expertise Files
```
.claude/commands/experts/<domain>/expertise.yaml
```

### Expert Commands
```
.claude/commands/experts/<domain>/question.md
.claude/commands/experts/<domain>/plan.md
.claude/commands/experts/<domain>/build.md
.claude/commands/experts/<domain>/self-improve.md
.claude/commands/experts/<domain>/plan_build_improve.md
```

### Agents
```
.claude/agents/<agent-name>.md
```

### Skills
```
.claude/skills/<skill-name>.md
```

## Creating New Domains

To create a new expert domain:

1. **Create domain directory:**
   ```bash
   mkdir -p .claude/commands/experts/<domain>
   ```

2. **Create expertise.yaml:**
   ```bash
   touch .claude/commands/experts/<domain>/expertise.yaml
   ```
   Populate with four-pillar structure (Information, Examples, Patterns, Expertise)

3. **Create command files:**
   - Start with `question.md` for Q&A capability
   - Add `plan.md` for planning capability
   - Add `build.md` for building capability
   - Add `self-improve.md` for self-improvement
   - Optionally add `plan_build_improve.md` for chained workflows

4. **Create agent (optional):**
   ```bash
   touch .claude/agents/<domain>-expert.md
   ```
   Configure agent to delegate to domain commands

## File Dependencies

### Command Dependencies
- All commands depend on `expertise.yaml` in their domain
- `build.md` depends on output from `plan.md`
- `self-improve.md` depends on codebase changes
- `plan_build_improve.md` depends on `plan.md`, `build.md`, and `self-improve.md`

### Agent Dependencies
- Agents depend on commands they delegate to
- Domain expert agents depend on their domain's commands
- Meta-agents depend on file system write access

### Skill Dependencies
- Skills are self-contained
- Referenced by agents but not directly invoked
- Can reference commands if needed

## Validation Checklist

Before deploying a new domain, verify:

- [ ] Domain directory exists: `.claude/commands/experts/<domain>/`
- [ ] `expertise.yaml` exists and follows four-pillar structure
- [ ] At least one command file exists (`question.md` recommended)
- [ ] Command files have correct frontmatter
- [ ] Command files reference `EXPERTISE_PATH` correctly
- [ ] Agent file exists (optional but recommended)
- [ ] Agent file has correct frontmatter and delegates to commands
- [ ] All files follow naming conventions
- [ ] Invocation syntax works: `/experts:<domain>:<action>`

## Common Patterns

### Minimal Domain Setup
```
.claude/commands/experts/<domain>/
├── expertise.yaml
└── question.md
```

### Standard Domain Setup
```
.claude/commands/experts/<domain>/
├── expertise.yaml
├── question.md
├── plan.md
├── build.md
└── self-improve.md
```

### Complete Domain Setup
```
.claude/commands/experts/<domain>/
├── expertise.yaml
├── question.md
├── plan.md
├── build.md
├── self-improve.md
└── plan_build_improve.md
```

Plus agent:
```
.claude/agents/<domain>-expert.md
```

## Notes

- All paths are relative to project root
- Domain names should be lowercase, descriptive, singular (e.g., `database` not `databases`)
- File names should match their function clearly
- Keep directory structure flat - avoid nested subdirectories within domains
- Use consistent naming across all domains for easier discovery

