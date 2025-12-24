# Handoff

Emit a formal handoff contract exactly as defined in `directives/HANDOFF_PROTOCOL.md`.

## Action

When transferring work between agents or to MetaGPT, emit a complete handoff contract JSON.

## Required Fields

```json
{
  "handoff_id": "unique-id",
  "from_agent": "agent-name",
  "to_agent": "agent-name|METAGPT",
  "timestamp": "ISO-8601-timestamp",
  "status": "success|blocked|failed",
  "produced_artifacts": [
    {
      "type": "file|data|decision",
      "location": "path/to/artifact",
      "description": "brief description"
    }
  ],
  "assumptions": [
    {
      "assumption": "assumption text",
      "validated": true|false,
      "risk": "low|medium|high"
    }
  ],
  "missing_inputs": [
    {
      "required": "input description",
      "reason": "why needed",
      "blocking": true|false
    }
  ],
  "recommended_next_agent": "agent-name|USER_INPUT_REQUIRED",
  "context_summary": "one paragraph summary",
  "kb_updates_proposed": true|false,
  "session_id": "session-uuid"
}
```

## Status Values

- **success**: Task completed successfully, artifacts ready
- **blocked**: Task cannot proceed without missing inputs
- **failed**: Task failed, retry or terminate

## Enforcement

- Handoff contract must be complete (all required fields)
- Status must be terminal (not "in_progress")
- Artifacts must match task objective
- Assumptions must be documented

## Notes

- MetaGPT evaluates handoff and routes to next agent or user
- Incomplete handoffs are rejected
- See `directives/HANDOFF_PROTOCOL.md` for full specification

