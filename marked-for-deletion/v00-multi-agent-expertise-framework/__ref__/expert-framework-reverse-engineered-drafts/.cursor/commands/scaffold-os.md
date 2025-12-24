# Scaffold OS

Regenerate the file-based agentic workflow OS structure.

## Action

Execute `python scripts/scaffold_os.py --apply --force` to regenerate the scaffold.

## When to Use

- Initial setup
- After structural changes to the OS
- To restore missing directories/files

## Dry Run First

Before applying, you can preview changes:
```bash
python scripts/scaffold_os.py --dry-run
```

## Review Generated Diffs

After running, review what was created/modified:
- New directories
- New files
- Updated files

## Notes

- Use `--force` to overwrite existing files (be careful)
- Generated files should be reviewed before committing
- Consider staging the scaffold output in `review-approval/` for review

