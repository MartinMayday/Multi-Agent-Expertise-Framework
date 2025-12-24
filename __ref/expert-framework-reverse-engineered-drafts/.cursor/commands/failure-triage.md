# Failure Triage

Standard failure response protocol: reproduce, isolate, propose minimal fix, add validation steps, record next actions.

## Action

When a failure occurs, follow this protocol:

## Steps

1. **Reproduce**: 
   - Can you reproduce the failure?
   - What exact steps trigger it?
   - What is the error message/output?

2. **Isolate**:
   - What component failed?
   - Is it a tool, workflow, directive, or agent behavior?
   - What are the minimal conditions to trigger the failure?

3. **Propose Minimal Fix**:
   - What is the smallest change that fixes the issue?
   - Does the fix introduce new risks?
   - Is the fix reversible?

4. **Add Validation Steps**:
   - How can we test the fix?
   - What validation should run before/after?
   - How do we prevent regression?

5. **Record Next Actions**:
   - Document the failure in appropriate location
   - Update `planning/WORKSESSION_STATE.md` with failure status
   - Propose next steps (fix, retry, or escalate)

## Output Format

```markdown
## Failure Summary
- **Component**: [what failed]
- **Error**: [error message]
- **Reproducible**: yes|no
- **Isolated to**: [component/area]

## Proposed Fix
- **Change**: [minimal fix description]
- **Risk**: low|medium|high
- **Reversible**: yes|no

## Validation
- **Test steps**: [how to validate fix]
- **Prevention**: [how to prevent regression]

## Next Actions
- [ ] Apply fix (staged in review-approval/)
- [ ] Run validation
- [ ] Update documentation
- [ ] Record in planning/WORKSESSION_STATE.md
```

## Notes

- Don't skip steps - thorough triage prevents repeated failures
- Minimal fixes reduce risk
- Always add validation to catch regressions

