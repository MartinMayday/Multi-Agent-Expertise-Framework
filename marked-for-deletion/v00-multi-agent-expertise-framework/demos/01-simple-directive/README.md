# Demo 01: Simple Directive

This demo shows a minimal directive implementation.

## Steps
1. Read `directive.yaml`.
2. Observe the clear purpose and variables.
3. Run the "agent" (mocked) to see it follow the instruction.

```yaml
name: "hello_world"
description: "Simple test directive"
variables:
  NAME: $1
workflow:
  - step: 1
    action: "log"
    message: "Hello, {{NAME}}!"
```
