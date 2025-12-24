# Create Execution Workflow

Scaffold a workflow in `executions/workflows/` plus any required directive stub in `directives/`.

## Action

Create a new workflow following the workflow pattern.

## Required Information

1. **Workflow Specification**:
   - What is the workflow's purpose?
   - What steps does it contain?
   - What tools/workflows does it call?
   - What are the inputs/outputs?

2. **Workflow Structure**:
   - Workflow file in `executions/workflows/`
   - Directive stub in `directives/` (if needed)
   - Documentation

## Template Structure

```
executions/workflows/<workflow-name>/
├── <workflow-name>.py      # Workflow implementation
├── README.md               # Workflow documentation
└── directives/             # Related directive stubs (if needed)
```

## Workflow Requirements

- **Sequential steps**: Clear step-by-step execution
- **Error handling**: Handle failures at each step
- **State management**: Track workflow state
- **Handoff support**: Can emit handoff contracts
- **Documentation**: Clear usage and step descriptions

## Directive Integration

If the workflow needs behavior contracts:
- Create directive stub in `directives/`
- Reference directive in workflow documentation
- Follow directive format from `directives/*.md`

## Output Location

Write to `review-approval/` first, then promote to `executions/workflows/` after approval.

## Notes

- Workflows should call execution tools, not implement logic directly
- See `directives/templates/plan_build_improve.md` for workflow pattern
- Follow existing workflow patterns in `executions/workflows/`

