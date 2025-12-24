# ❌ Anti-Patterns

## 1. Blind Trust
Trusting documentation or expertise files without validating them against the actual codebase implementation.

## 2. Context Dumping
Loading entire files or directories into the LLM context when only specific sections are needed.

## 3. Parallel Dependencies
Attempting to run steps in parallel when they have sequential dependencies (e.g., building before planning is complete).

## 4. Secret Exposure
Committing API keys, tokens, or PII into the repository or context memory files.
