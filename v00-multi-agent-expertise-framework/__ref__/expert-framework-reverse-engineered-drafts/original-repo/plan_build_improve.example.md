---
allowed-tools: Task, TaskOutput, TodoWrite
description: Complete WebSocket implemantation workflow - plan, build, and self-improve
argument: [websocket_implementation_request] [human_in_the_loop (bool)]
---

# Purpose

This workflow orchestrates a complete WebSocket implementation cycle by chaining three specialized commands: expertise-informed planning, building from the plan, and self-improving the expertise based on changes made.

## Variables

USER_PROMPT: $1
HUMAN_IN_THE_LOOP: $2 or true if not specified

## Instructions

- Execute steps 1-3 sequentially using the Task tool for each step
- Each subagent starts fresh with no prior context - provide complete instructions
- Use TaskOutput to retrieve results before proceeding to the next step
- DO NOT STOP between steps - complete the entire workflow


## Workflow

### Step 1: Create Plan

Spawn a subagent to run planning command:

    ```
        Task(
        subagent_type: "general-purpose",
        prompt: "Run SlashCommand('/experts:websocket:plan [USER_PROMPT]'). Return the path to the generated plan file."
    )
    ```
Replace `[USER_PROMPT]` with the actual user request.

Use TaskOutput to get `path_to_plan` before proceeding.


### Step 2: Build

Spawn a subagent to run build command:

    ```
    Task(
        subagent_type: "general-purpose",
        prompt: "Run SlashCommand('/experts:websocket:plan [USER_PROMPT]'). Return the path to the generated plan file."
    )
    ```
Replace `[path_to_plan]` with the path from Step 1.

Use TaskOutput to get `build_report` before proceeding.

### Step 3: Self-Improve

    ```
    Task(
        subagent_type: "general-purpose",
        prompt: "Run SlashCommand('/experts:websocket:plan [USER_PROMPT]'). Return the path to the generated plan file."
    )
    ```

Use TaskOutput to get `self_improve_report` before proceeding.


### Step 4: Report

    ```
    Task(
        subagent_type: "general-purpose",
        prompt: "Run SlashCommand('/experts:websocket:plan [USER_PROMPT]'). Return the path to the generated plan file."
    )
    ```

Use TaskOutput to get `path_to_report` before proceeding.

## Report


Use example:
/experts:websocket:plan_build_improve "Add a session-based counter to the app nav bar that displays the total number of WebSocket events received during the current session."