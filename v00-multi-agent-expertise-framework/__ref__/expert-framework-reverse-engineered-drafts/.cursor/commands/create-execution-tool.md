# Create Execution Tool

Scaffold a new deterministic Python tool in `executions/tools/` with minimal docs and validation hook.

## Action

Create a new Python tool following the execution tool pattern.

## Required Information

1. **Tool Specification**:
   - What does the tool do?
   - What are the inputs?
   - What are the outputs?
   - What validation does it perform?

2. **Tool Structure**:
   - Main Python file in `executions/tools/`
   - README.md documenting usage
   - Test file (if applicable)
   - Validation hook

## Template Structure

```
executions/tools/<tool-name>/
├── <tool-name>.py          # Main tool implementation
├── README.md               # Usage documentation
└── test_<tool-name>.py     # Tests (optional)
```

## Tool Requirements

- **Deterministic**: Same inputs → same outputs
- **No assumptions**: Require all inputs via parameters or config
- **Validation**: Validate inputs and outputs
- **Error handling**: Graceful failures with clear messages
- **Documentation**: Clear usage instructions

## Output Location

Write to `review-approval/` first, then promote to `executions/tools/` after approval.

## Notes

- Do NOT invent behavior - require spec inputs
- Tools must be testable
- Follow existing tool patterns in `executions/tools/`
- See `executions/README.md` for tool conventions

