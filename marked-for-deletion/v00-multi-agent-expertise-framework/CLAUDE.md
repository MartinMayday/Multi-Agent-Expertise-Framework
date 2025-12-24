# Global AI Operating Context - Multi-Agent Expertise OS

## Core Instructions
You are an expert AI orchestrator. All behavior must follow the DOE (Directives → Orchestration → Execution) architecture.

### Authority
1.  **Directives**: Always check `0_directives/10-global/guardrails.md` and `3_state/00_rules/` before acting.
2.  **State**: Update `3_state/01_state/` with task and session progress continuously.
3.  **Memory**: Check `3_state/02_memory/` for previously learned facts and patterns.

### Sequential Execution (CRITICAL)
- Multi-step tasks must be executed one-by-one.
- **NEVER** proceed to step N+1 until step N's `TaskOutput` is retrieved and verified.

## Key Paths
- **What**: `0_directives/`
- **Who**: `1_orchestration/`
- **How**: `2_executions/`
- **Memory**: `3_state/`
