# Validate Scaffold

Run scaffold validation and interpret results.

## Action

Execute `python scripts/validate_scaffold.py --project-root . -v` and analyze the output.

## Expected Output

1. **Validation Results**: Report which checks passed/failed
2. **Failure Analysis**: For each failure, identify:
   - What is missing or incorrect
   - Why it matters
   - How to fix it
3. **Fix Plan**: Propose specific steps to resolve failures

## Validation Checks

The script validates:
- Directory structure (all required directories exist)
- Core directives (KB_GUARDRAILS, HANDOFF_PROTOCOL, PROGRESSIVE_LOADING, FAILURE_HANDLING, STAGING_AND_APPROVAL)
- Agent scaffolding (all 7 agents have required files)
- KB structure (manifest.md, snippet format)
- Root documentation (FRAMEWORK.md, AGENTIC_WORKFLOW_CONTRACT.md, etc.)

## Notes

- If validation fails, create a fix plan before proceeding
- All fixes must be staged in `review-approval/` before promotion

