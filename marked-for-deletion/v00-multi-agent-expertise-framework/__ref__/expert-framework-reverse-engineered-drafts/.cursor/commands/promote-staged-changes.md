# Promote Staged Changes

Run promotion tool, require validation + approval before moving files from staging to canonical locations.

## Action

Promote staged changes only after:
1. Validation passes
2. Approval checklist completed
3. Human approval granted

## Pre-Promotion Checks

1. **Validation**:
   - Run `python scripts/validate_scaffold.py --project-root . -v`
   - Run relevant tests (if applicable)
   - Check for secrets/sensitive data

2. **Approval Checklist**:
   - Scaffold validation passes
   - All tests pass (if applicable)
   - No secrets or sensitive data
   - Files follow filesystem-as-API contract
   - KB snippets have proper source attribution
   - Documentation updated if needed

3. **Human Approval**:
   - Approval status in changeset.yaml must be "approved"
   - Approved by and approved_at must be set

## Promotion Process

1. Read `review-approval/changeset.yaml`
2. Verify all checks pass
3. Move files from staging to canonical locations
4. Update changeset with promotion timestamp
5. Run post-promotion validation
6. Update `planning/REVIEW_APPROVAL_QUEUE.md`

## Rollback

If post-promotion validation fails:
- Attempt rollback if possible
- Log failure
- Update changeset status

## Notes

- Promotion is irreversible (be careful)
- Always validate before and after promotion
- Update planning state after promotion
- See `directives/STAGING_AND_APPROVAL.md` for full protocol

