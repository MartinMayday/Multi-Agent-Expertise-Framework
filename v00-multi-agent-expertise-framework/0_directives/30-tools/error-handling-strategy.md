# Error Handling Strategy

## 1. Autonomous Retry
Transient errors (RateLimit, ServerError, Timeout) are handled with a 6-attempt distribution over 10 minutes with ±30% jitter.

## 2. Escalation
If a tool fails after all retries, the incident must be logged in `3_state/errors/incidents/` and a human handoff must be triggered.

## 3. Rollback
Failed implementations that leave the codebase in an unstable state must be rolled back using the `03_archive/` session state.
