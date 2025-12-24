---
directive_id: AGENT_HOOKS
version: 1.0
enforcement_level: OPTIONAL
applies_to: ALL_AGENTS
bypass_allowed: true
validation_checkpoint: POST_EXECUTION
---

# Agent Hooks

## Purpose
Agent hooks provide extension points for custom behavior during agent execution lifecycle.

## Hook Types

### Pre-Execution Hooks
- **When**: Before agent processes task
- **Location**: executions/hooks/pre_execution.py
- **Can**: Modify input, validate prerequisites
- **Cannot**: Skip KB-first checks

### Post-Execution Hooks
- **When**: After agent completes task
- **Location**: executions/hooks/post_execution.py
- **Can**: Update KB, log metrics, trigger notifications
- **Cannot**: Modify agent output

### Error Hooks
- **When**: On agent failure
- **Location**: executions/hooks/on_error.py
- **Can**: Log errors, attempt recovery, notify
- **Cannot**: Suppress errors

## Implementation

Hooks are Python modules that implement standard interfaces:

```python
def pre_execution(agent_name: str, task: dict) -> dict:
    # Modify task if needed
    return task

def post_execution(agent_name: str, result: dict) -> None:
    # Process result
    pass

def on_error(agent_name: str, error: Exception) -> None:
    # Handle error
    pass
```

## Configuration

Hooks are optional. To enable:
1. Create hook module in executions/hooks/
2. Register in agent's mcp.json or system config
3. Ensure hook follows contract (read-only unless explicitly granted write)

## Contract

Hooks must:
- Not modify agent system-instructions.md
- Not bypass directives
- Log all actions
- Fail gracefully if dependencies unavailable
