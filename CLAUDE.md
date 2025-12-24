# Global AI Operating Context

## Core Instructions

You are an expert AI agent working within the **Multi-Agent Expertise Framework**. Your behavior is governed by the DOE (Directives → Orchestration → Execution) pattern.

### Authority Order

1. **Directives**: Always check `0_directives/core/rules.md` and `3_state/.context/core/rules.md` first.
2. **Context**: Load Elle context layers progressively.
3. **Execution**: Use pre-built tools in `2_executions/tools/` for all technical tasks.

### Workflow Protocol

- **KB-First**: Before answering or acting, search the `1_orchestration/knowledge/` and `3_state/` for existing expertise.
- **Validation**: Never trust documentation blindly. Use `Grep` or `Read` to validate against the codebase.
- **Handoff**: If transitioning tasks, emit a formal handoff contract.
- **Staging**: All file modifications must be written to `staging/` first for approval.

## Essential Commands

- `/experts:<domain>:plan`
- `/experts:<domain>:build`
- `/experts:<domain>:self-improve`
- `@agent-metagpt`
- `@agent-researchgpt`

Refer to `AGENTS.md` for the full capability index.
