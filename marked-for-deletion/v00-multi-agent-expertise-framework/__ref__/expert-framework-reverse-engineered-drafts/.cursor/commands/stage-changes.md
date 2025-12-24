# Stage Changes

Create changeset.yaml and stage outputs in review-approval/ or staging/.

## Action

When generating new or modified files:
1. Write files to `review-approval/` (for human review) or `staging/` (for machine outputs)
2. Create or update `review-approval/changeset.yaml`
3. Document what changed, why, and target promotion paths

## Changeset Format

See `review-approval/changeset.yaml` template for required fields:
- `changeset_id`: Unique identifier
- `timestamp`: ISO 8601 timestamp
- `author`: Agent/user identifier
- `description`: What changed and why
- `files`: List of files with source (staging) and target (canonical) paths
- `validation_status`: Results of validation checks
- `approval_required`: Boolean flag
- `promotion_checklist`: Required checks before promotion

## File Organization

- **Human-reviewed changes**: `review-approval/`
  - New/modified files
  - Changeset YAML
  - Optional patches/diffs

- **Machine outputs**: `staging/`
  - Tool outputs
  - Generated files
  - Temporary artifacts

## Notes

- All new/changed files MUST go to staging first
- Changeset is required for all staged changes
- Don't skip changeset creation - it's the audit trail

