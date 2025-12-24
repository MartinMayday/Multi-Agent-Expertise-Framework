# Plan-Build-Self-Improve

Execute the complete plan → build → self-improve loop using existing templates in `directives/templates/`.

## Action

Orchestrate the three-step workflow:
1. **Plan**: Create implementation plan using domain expertise
2. **Build**: Execute the plan
3. **Self-Improve**: Update expertise based on learnings

## Workflow Steps

### Step 1: Plan

Use template: `directives/templates/plan.md`

- Read relevant expertise/knowledge
- Create detailed implementation plan
- Document assumptions and risks
- Stage plan in `review-approval/` for approval (if human-in-the-loop)

### Step 2: Build

Use template: `directives/templates/build.md`

- Execute plan step-by-step
- Use execution tools from `executions/`
- Stage outputs in `staging/out/`
- Validate at each step

### Step 3: Self-Improve

Use template: `directives/templates/self-improve.md`

- Analyze what worked/didn't work
- Update expertise/knowledge base
- Generate KB snippets for new learnings
- Update agent manifests if needed

## Chained Workflow

See `directives/templates/plan_build_improve.md` for the complete chained workflow pattern.

## Variables

- `USER_PROMPT`: Implementation request
- `HUMAN_IN_THE_LOOP`: Pause for approval after plan (default: true)

## Output Locations

- Plans: `planning/` or `review-approval/`
- Build outputs: `staging/out/`
- Improvements: `shared-knowledgebase/snippets/` (after approval)

## Notes

- Each step must complete before next step
- Use Task/TaskOutput for subagent orchestration
- Self-improvement is mandatory - don't skip it
- All changes must be staged before promotion

