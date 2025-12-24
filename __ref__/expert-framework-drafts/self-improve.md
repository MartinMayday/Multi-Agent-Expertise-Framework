---
allowed-tools: Bash, Read, Grep, Glob, Write, TodoWrite
description: Self-improve domain expertise by validating against codebase implementation
argument: [check_git_diff (true/false)] [focus_area (optional)]
---

# Purpose

Maintain the expert system's expertise accuracy by comparing the existing expertise file against the actual codebase implementation. This command detects differences, missing pieces, or outdated information, and updates the expertise file to ensure it remains a powerful **mental model** and accurate memory reference for domain-related tasks.

## Variables

USER_PROMPT: $1 (optional focus area or validation scope)
CHECK_GIT_DIFF: $2 or false if not specified
FOCUS_AREA: $3 (optional: specific area to focus validation on)
EXPERTISE_PATH: .claude/commands/experts/<domain>/expertise.yaml

## Instructions

- Read the current `EXPERTISE_PATH` file to understand existing expertise
- Search and analyze the codebase to validate expertise accuracy
- Compare expertise claims against actual implementation
- Identify discrepancies, missing information, or outdated patterns
- If `CHECK_GIT_DIFF` is true, check git diff to see what changed recently
- If `FOCUS_AREA` is specified, prioritize validation in that area
- Update `EXPERTISE_PATH` with corrected, missing, or new information
- Preserve valid expertise while updating inaccurate information
- Ensure expertise file maintains four-pillar structure (Information, Examples, Patterns, Expertise)

## Workflow

1. Read `EXPERTISE_PATH` to load current expertise knowledge
2. If `CHECK_GIT_DIFF` is true:
   - Run `git diff` to identify recent code changes
   - Focus validation on changed areas
3. If `FOCUS_AREA` is specified:
   - Narrow validation scope to focus area
4. For each section in expertise (Information, Examples, Patterns, Expertise):
   - Search codebase for evidence supporting expertise claims
   - Validate examples still exist and are accurate
   - Verify patterns are still used correctly
   - Check for new patterns not yet documented
5. Identify discrepancies:
   - Outdated information
   - Missing examples
   - New patterns not documented
   - Incorrect patterns or anti-patterns
6. Update `EXPERTISE_PATH`:
   - Correct outdated information
   - Add missing examples
   - Document new patterns
   - Update expertise guidelines
7. Validate updated expertise file structure
8. Generate self-improvement report

## Report

- Summary of validation findings
- List of discrepancies identified
- Updates made to expertise file
- New patterns or examples discovered
- Areas that remain accurate
- Recommendations for future validation

Use example:
/experts:database:self-improve true "schema_changes"
/experts:websocket:self-improve false

