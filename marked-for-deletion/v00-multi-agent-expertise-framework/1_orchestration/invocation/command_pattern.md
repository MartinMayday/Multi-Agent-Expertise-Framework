# Command Invocation Pattern

## Format
`/experts:<domain>:<action> [arguments]`

## Examples
- `/experts:database:question "How does information flow between tables?"`
- `/experts:websocket:plan "Add session-based counter"`
- `/experts:websocket:plan_build_improve "Implement WebSocket event tracking"`
- `/experts:api:self-improve`

## Actions
- `question`: Q&A mode with expertise validation.
- `plan`: Generate implementation plan.
- `build`: Implement code from plan.
- `self-improve`: Validate and update expertise.
- `plan_build_improve`: Full 3-phase orchestration cycle.
