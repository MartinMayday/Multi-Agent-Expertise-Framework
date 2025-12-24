---
name: Repository Workflows
description: Standard operating procedures — how this repository does recurring things.
update_policy: Update when a workflow is learned or changed. Add new categories as needed. No permission required.
---

## Change Management Workflow

### Making Changes

<guide>Standard process for making any change</guide>

1. **Stage changes** → Write to `review-approval/` or `staging/`
2. **Create changeset** → Document in `review-approval/changeset.yaml`
3. **Run validation** → `python scripts/validate_scaffold.py --project-root . -v`
4. **Get approval** → Human reviews and approves
5. **Promote** → Use `/promote-staged-changes` or manual promotion

### Staging Workflow

<guide>How to stage changes</guide>

1. Write new/modified files to `review-approval/` (for human review) or `staging/` (for machine outputs)
2. Create or update `review-approval/changeset.yaml`
3. Document: what changed, why, target canonical paths
4. Wait for validation + approval
5. Promote after approval

## Development Workflows

### Adding New Agent

<guide>How to add a new agent to the system</guide>

1. Create agent directory: `agents/<agentname>/`
2. Create system instructions: `agents/<agentname>/<agentname>_system-instructions.md`
3. Create KB manifest: `agents/<agentname>/kb_<agentname>-manifest.md`
4. Create MCP config: `agents/<agentname>/mcp.json`
5. Create .env.example: `agents/<agentname>/.env.example`
6. Update `AGENTS.md` catalog
7. Stage all changes in `review-approval/`
8. Validate and promote

### Adding New Directive

<guide>How to add a new behavior directive</guide>

1. Create directive file: `directives/<DIRECTIVE_NAME>.md`
2. Follow directive format (frontmatter + execution sequence)
3. Update `directives/README.md`
4. Update `AGENTIC_WORKFLOW_CONTRACT.md` if needed
5. Stage in `review-approval/`
6. Validate and promote

### Adding New Execution Tool

<guide>How to add a new Python tool</guide>

1. Create tool directory: `executions/tools/<tool-name>/`
2. Create main Python file: `executions/tools/<tool-name>/<tool-name>.py`
3. Create README: `executions/tools/<tool-name>/README.md`
4. Create tests (optional): `executions/tools/<tool-name>/test_<tool-name>.py`
5. Update `executions/README.md`
6. Stage in `review-approval/`
7. Validate and promote

## Context Update Workflow

### Updating Context

<guide>How to update .context/ files</guide>

1. **Check rules first** → Always read `.context/core/rules.md` before actions
2. **Update session** → Update `.context/core/session.md` with current focus
3. **Detect corrections** → If user corrects behavior, add to `rules.md` immediately
4. **Update preferences** → If new preference learned, update `preferences.md` (replace old if contradicts)
5. **Update projects** → If project status changed, update `projects.md`
6. **Append journal** → At end of notable session, append to `journal.md` (newest first)
7. **Create transcript** → After session, create transcript in `conversations/`

### Creating Transcripts

<guide>How to create conversation transcripts</guide>

1. After session ends, create file: `.context/conversations/[session-id]-[timestamp].md`
2. Include frontmatter: session_id, timestamp, participants, tools_used, redactions
3. Include full transcript content
4. **Never modify** after creation (append-only)

## Validation Workflow

### Pre-Promotion Validation

<guide>What to validate before promoting changes</guide>

1. **Scaffold validation** → `python scripts/validate_scaffold.py --project-root . -v`
2. **Context validation** → `python executions/tools/context_validator/validate_context_tree.py` (once implemented)
3. **Test execution** → Run relevant tests if applicable
4. **Secret check** → Verify no secrets or sensitive data
5. **Contract compliance** → Verify files follow filesystem-as-API contract

## Knowledge Base Workflow

### Adding KB Snippets

<guide>How to add knowledge to shared-knowledgebase</guide>

1. Check `shared-knowledgebase/manifest.md` for duplicates
2. Create snippet following format: `shared-knowledgebase/frameworks/kb_snippet_format.md`
3. Include frontmatter: id, title, source_type, source_url, confidence, tags
4. Include: Summary, Verified Facts, Non-Facts, Implications
5. Stage in `review-approval/`
6. Validate and promote

## Handoff Workflow

### Agent-to-Agent Handoff

<guide>How agents transfer work</guide>

1. Agent A reaches terminal state (completed/blocked/failed)
2. Agent A emits handoff contract JSON (see `directives/HANDOFF_PROTOCOL.md`)
3. MetaGPT evaluates and routes
4. Agent B receives handoff contract + workflow state
5. Agent B updates `.context/core/session.md` with new focus

## Evaluation Workflow

### Running Evaluations

<guide>How to evaluate agent performance</guide>

1. Check if evaluation tooling exists: `executions/eval/`
2. If exists, run evaluation tool
3. If not, create spec and request tool creation
4. Update maturity scores in `agents/<agent>/eval/`
5. Update `.context/core/journal.md` with evaluation results

