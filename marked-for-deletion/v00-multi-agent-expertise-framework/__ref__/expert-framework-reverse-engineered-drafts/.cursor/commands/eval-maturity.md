# Eval Maturity

Run or request evaluation tooling for agent maturity scoring.

## Action

If evaluation tooling exists in `executions/eval/`, run it. Otherwise, create a spec and request for evaluation tooling.

## Check for Existing Tooling

1. Check `executions/eval/` for existing evaluation tools
2. Check `executions/README.md` for eval tool documentation
3. Check agent `eval/` directories for agent-specific metrics

## If Tooling Exists

Run the evaluation:
- Execute the tool with appropriate parameters
- Collect results
- Update maturity scores
- Document findings

## If Tooling Does NOT Exist

**DO NOT pretend it exists**. Instead:

1. **Create Spec**:
   - What metrics should be evaluated?
   - What is the evaluation methodology?
   - What are the success criteria?

2. **Request Tool Creation**:
   - Use `/create-execution-tool` to scaffold evaluation tool
   - Document evaluation requirements
   - Stage in `review-approval/` for approval

## Evaluation Metrics

Common metrics:
- Agent reliability (success rate)
- Knowledge completeness (KB coverage)
- Response quality (validation against KB)
- Tool correctness (execution tool accuracy)
- Handoff success rate

## Output Location

Evaluation results go to:
- Agent-specific: `agents/<agent>/eval/`
- Global: `eval/`
- Staging: `staging/out/eval/` (if temporary)

## Notes

- Don't claim evaluation ran if tooling doesn't exist
- Evaluation tools must be deterministic and testable
- See `directives/AGENT_HOOKS.md` for evaluation trigger points

