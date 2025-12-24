# Team & Roles

## Team Structure
- **Project Owner**: Responsible for vision, requirements, approval
- **Framework Maintainer**: Maintains DOE structure, memory system, orchestration
- **Agent Developers**: Develop specialized agents and skills
- **QA Engineer**: Verifies workflows, tests, validation

## Communication Protocols

### Async
- Decision logs in `3_state/02_memory/decisions.log.md`
- PRs with detailed descriptions
- Comments in code for non-obvious decisions

### Sync
- Weekly planning sessions (if applicable)
- Code review before merge
- Architecture discussions documented

## Decision Making

All significant decisions (architectural, dependency changes, breaking API changes) must:
1. Be discussed and documented in ADR format
2. Be added to `3_state/02_memory/decisions.log.md`
3. Be committed with the change

## Escalation Path
- Blocker → mention in task_queue.json blockers field
- Major decision → create ADR
- Breaking change → discussion required before implementation
