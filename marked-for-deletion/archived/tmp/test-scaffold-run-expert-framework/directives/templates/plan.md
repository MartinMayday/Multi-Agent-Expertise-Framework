---
allowed-tools: Read, Write, Grep, Glob, TodoWrite
description: Create a structured implementation plan using domain expertise
argument-hint: [implementation_request]
---

# Purpose

Create a structured, actionable implementation plan by leveraging domain expertise stored in the expertise file. This plan serves as the blueprint for implementation and should reference existing patterns, best practices, and architectural principles from the expertise knowledge base.

## Variables

USER_PROMPT: $1
EXPERTISE_PATH: .claude/commands/experts/<domain>/expertise.yaml
PLAN_OUTPUT_PATH: temp/<domain>_plan_<timestamp>.md

## Instructions

- Read the `EXPERTISE_PATH` file to understand domain architecture, patterns, and best practices
- Analyze the `USER_PROMPT` to understand the implementation requirements
- Create a structured plan that follows patterns from the expertise file
- Reference existing code examples and patterns where applicable
- Include file paths, code structure, and implementation steps
- Validate plan against expertise guidelines before finalizing
- Write the plan to `PLAN_OUTPUT_PATH` for review and execution

## Workflow

1. Read `EXPERTISE_PATH` to load domain expertise (Information, Examples, Patterns, Expertise)
2. Analyze `USER_PROMPT` to extract requirements and scope
3. Search codebase for related implementations using patterns from expertise
4. Create structured plan following this format:
   - **Overview**: High-level summary of what will be implemented
   - **Architecture**: How it fits into existing system (reference expertise patterns)
   - **Implementation Steps**: Detailed step-by-step breakdown
   - **Files to Create/Modify**: List of files with brief descriptions
   - **Patterns to Follow**: Reference specific patterns from expertise
   - **Validation**: How to verify the implementation
   - **Dependencies**: What needs to be in place first
5. Validate plan against expertise guidelines and best practices
6. Write plan to `PLAN_OUTPUT_PATH`
7. Return path to plan file

## Report

- Path to generated plan file
- Brief summary of plan structure
- Key patterns and expertise references used
- Estimated complexity and dependencies

Use example:
/experts:websocket:plan "Add a session-based counter to the app nav bar that displays the total number of WebSocket events received during the current session."

