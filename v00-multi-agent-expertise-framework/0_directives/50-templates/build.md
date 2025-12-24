---
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
description: Implement code changes based on a structured plan
argument-hint: [path_to_plan]
---

# Purpose

Implement code changes following a structured plan created by the planning command. This command reads the plan, follows the implementation steps, and creates or modifies code files according to the plan's specifications while adhering to domain expertise patterns.

## Variables

PLAN_PATH: $1
EXPERTISE_PATH: .claude/commands/experts/<domain>/expertise.yaml

## Instructions

- Read the `PLAN_PATH` file to understand the implementation requirements
- Read `EXPERTISE_PATH` to ensure implementation follows domain patterns
- Execute implementation steps from the plan sequentially
- Follow code patterns and examples from the expertise file
- Create or modify files as specified in the plan
- Validate code against expertise guidelines as you implement
- Do not skip steps - implement all items in the plan
- If plan references patterns, ensure they are followed correctly

## Workflow

1. Read `PLAN_PATH` to load implementation plan
2. Read `EXPERTISE_PATH` to load domain expertise and patterns
3. For each implementation step in the plan:
   - Identify files to create or modify
   - Review relevant code examples from expertise
   - Implement following patterns and best practices
   - Validate against expertise guidelines
4. Create new files as specified in plan
5. Modify existing files following plan specifications
6. Ensure all dependencies are addressed
7. Validate implementation matches plan requirements
8. Generate build report with summary of changes

## Report

- Summary of files created
- Summary of files modified
- Key implementation decisions
- Patterns followed from expertise
- Validation results
- Any deviations from plan and rationale

Use example:
/experts:websocket:build temp/websocket_plan_20240101_120000.md

