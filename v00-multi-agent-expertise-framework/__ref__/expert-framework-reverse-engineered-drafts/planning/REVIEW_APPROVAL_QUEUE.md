# Review & Approval Queue

**Last Updated**: 2024-12-23

## Active Changesets

Currently no changesets pending approval.

## Approval Process

1. **Review Changeset**: Read `review-approval/changeset.yaml`
2. **Review Files**: Examine staged files in `review-approval/`
3. **Run Validation**: `python scripts/validate_scaffold.py --project-root . -v`
4. **Complete Checklist**: Verify all items in promotion_checklist
5. **Approve or Reject**: Update changeset.yaml with approval status
6. **Promote**: Use `/promote-staged-changes` command

## Promotion Checklist Template

For each changeset, verify:
- [ ] Scaffold validation passes
- [ ] All tests pass (if applicable)
- [ ] No secrets or sensitive data
- [ ] Files follow filesystem-as-API contract
- [ ] KB snippets have proper source attribution
- [ ] Documentation updated if needed

## History

### 2024-12-23
- **Changeset**: Initial staging system setup
- **Status**: ✅ Approved and promoted
- **Files**: review-approval/, staging/, directives/STAGING_AND_APPROVAL.md, .cursor/rules/project_rules.mdc, .cursor/commands/*, .cursorignore

---

## Notes

- Changesets remain in queue until approved or rejected
- Rejected changesets should be updated and resubmitted
- Approved changesets are promoted and archived

