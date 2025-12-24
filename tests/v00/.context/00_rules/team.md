# Team Structure - v00 Test Suite

## Roles

### Test Orchestrator
- **Responsibility**: Coordinate test execution and validation
- **Tools**: pytest, integration test runners
- **Success Metric**: All tests pass with >80% coverage

### Code Validator
- **Responsibility**: Run lint, type checks, basic tests
- **Tools**: ruff (linting), mypy (type checking)
- **Success Metric**: No errors, all checks pass

### Documentation Keeper
- **Responsibility**: Maintain test documentation and CHANGELOG
- **Tools**: Markdown editors
- **Success Metric**: All changes documented

## Communication Protocols

### Synchronous (When Used)
- Test results logged to `.context/01_state/task_queue.json`
- Failures reported in `.context/02_memory/decisions.log.md`

### Asynchronous
- Test status in `.context/01_state/active_session.json`
- Pattern analysis in `.context/02_memory/patterns.md`
- Session logs in `.context/03_archive/sessions/`

## Decision-Making

### Test Failures
1. Log error to event logger
2. Extract facts from logs
3. Check patterns for repeated failures
4. Mark blocker in task queue
5. Update decisions log with remediation plan

### Coverage Gaps
1. Identify untested code paths
2. Create test task in queue
3. Add to patterns for next iteration
4. Update progress in scratchpad

## Escalation

**When to Escalate**:
- Memory Ops system failures
- Scaffold generation errors
- Pattern recognizer producing invalid patterns

**Escalation Path**:
1. Document in `.context/02_memory/decisions.log.md`
2. Add detailed blocker to task queue
3. Reference main FRAMEWORK.md and architecture docs
