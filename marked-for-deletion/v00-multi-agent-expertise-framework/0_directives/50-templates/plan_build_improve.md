---
allowed-tools: Task, TaskOutput, TodoWrite
description: Complete implementation workflow - plan, build, and self-improve
argument: [implementation_request] [human_in_the_loop (bool)]
---

# Purpose

This workflow orchestrates a complete implementation cycle by chaining three specialized commands: expertise-informed planning, building from the plan, and self-improving the expertise based on changes made. This ensures that implementations follow domain expertise, and the expertise system learns from each implementation.

## Variables

USER_PROMPT: $1
HUMAN_IN_THE_LOOP: $2 or true if not specified

## Instructions

- Execute steps 1-3 sequentially using the Task tool for each step
- Each subagent starts fresh with no prior context - provide complete instructions
- Use TaskOutput to retrieve results before proceeding to the next step
- DO NOT STOP between steps - complete the entire workflow
- If HUMAN_IN_THE_LOOP is true, pause for approval after plan generation
- Ensure self-improvement runs after build to update expertise with new learnings

## Workflow

### Step 1: Create Plan

Spawn a subagent to run planning command:

```
Task(
    subagent_type: "general-purpose",
    prompt: "Run SlashCommand('/experts:<domain>:plan [USER_PROMPT]'). Return the path to the generated plan file."
)
```

Replace `[USER_PROMPT]` with the actual user request.
Replace `<domain>` with the appropriate domain (e.g., websocket, database, frontend).

Use TaskOutput to get `path_to_plan` before proceeding.

**If HUMAN_IN_THE_LOOP is true:** Present plan to user for approval before proceeding.

### Step 2: Build

Spawn a subagent to run build command:

```
Task(
    subagent_type: "general-purpose",
    prompt: "Run SlashCommand('/experts:<domain>:build [path_to_plan]'). Return the build report with summary of files created and modified."
)
```

Replace `[path_to_plan]` with the path from Step 1.
Replace `<domain>` with the appropriate domain.

Use TaskOutput to get `build_report` before proceeding.

### Step 3: Self-Improve

Spawn a subagent to run self-improve command:

```
Task(
    subagent_type: "general-purpose",
    prompt: "Run SlashCommand('/experts:<domain>:self-improve false'). Update the expertise file based on the implementation changes made in Step 2. Return the self-improvement report."
)
```

Replace `<domain>` with the appropriate domain.

Use TaskOutput to get `self_improve_report` before proceeding.

### Step 4: Report

Aggregate results from all steps into a final report:

```
Task(
    subagent_type: "general-purpose",
    prompt: "Create a comprehensive report summarizing:
    - The original request (USER_PROMPT)
    - The plan that was created (from Step 1)
    - The implementation that was built (from Step 2)
    - The expertise updates that were made (from Step 3)
    Write the report to temp/<domain>_workflow_report_<timestamp>.md and return the path."
)
```

Use TaskOutput to get `path_to_report` before proceeding.

## Report

- Path to final workflow report
- Summary of all steps completed
- Key outcomes from each phase
- Expertise updates made
- Files created/modified
- Next steps or recommendations

Use example:
/experts:websocket:plan_build_improve "Add a session-based counter to the app nav bar that displays the total number of WebSocket events received during the current session."

