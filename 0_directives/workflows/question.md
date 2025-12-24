---
allowed-tools: Read, Grep, Glob
argument-hint: [question]
---
# Purpose: Answer questions using expertise with codebase validation

## Variables
- USER_QUESTION: $1

## Instructions
- CRITICAL: Always validate expertise against codebase
- Expertise files are NOT authoritative - the codebase is

## Workflow
1. Read expertise.yaml
2. Search codebase to validate expertise claims
3. Identify discrepancies
4. Answer with validated information
5. Flag outdated expertise for self-improve

## Report
- Answer with source references
- Discrepancies identified
- Expertise update recommendations
