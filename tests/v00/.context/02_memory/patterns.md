# Detected Patterns - v00 Test Suite

## Format
Each pattern entry includes:
- **Name**: Pattern identifier
- **Description**: What was observed
- **Occurrences**: How many times detected
- **Confidence**: Likelihood (0.0-1.0)
- **Category**: Type of pattern
- **First Seen**: When first detected
- **Last Updated**: Most recent occurrence

---

## Common Test Patterns

### Pattern: JSON_VALIDATION_ERRORS
- **Description**: Schema validation failures in JSON files
- **Occurrences**: 0 (pending test execution)
- **Confidence**: 0.0
- **Category**: technical
- **Status**: Waiting for test data

### Pattern: SCAFFOLD_GENERATION_TIMING
- **Description**: Time taken to generate scaffold structure
- **Occurrences**: 0 (pending test execution)
- **Confidence**: 0.0
- **Category**: performance
- **Status**: Waiting for test data

### Pattern: CONTEXT_MERGE_CONFLICTS
- **Description**: Rule conflicts when merging global + project context
- **Occurrences**: 0 (pending test execution)
- **Confidence**: 0.0
- **Category**: technical
- **Status**: Waiting for test data

### Pattern: NDJSON_ATOMICITY_VIOLATIONS
- **Description**: Non-atomic writes to event log
- **Occurrences**: 0 (pending test execution)
- **Confidence**: 0.0
- **Category**: technical
- **Status**: Waiting for test data

---

## How Patterns Are Generated

1. **EventLogger** captures tool calls, decisions, and errors
2. **Session logs** stored in 03_archive/sessions/ as NDJSON
3. **PatternRecognizer** analyzes logs after test completion
4. **Patterns with 2+ occurrences** promoted to this file
5. **Confidence** calculated based on frequency and context

This file will be populated as tests run and patterns are detected.
