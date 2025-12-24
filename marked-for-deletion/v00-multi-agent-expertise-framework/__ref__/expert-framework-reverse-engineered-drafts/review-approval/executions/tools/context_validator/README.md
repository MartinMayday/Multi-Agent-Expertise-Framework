# Context Validator Tools

This directory contains deterministic Python tools for validating the `.context/` directory structure and transcript metadata.

## Tools

### `validate_context_tree.py`

Validates the `.context/` directory structure and required files.

**Usage:**
```bash
python executions/tools/context_validator/validate_context_tree.py [project-root]
```

**Checks:**
- Required core files exist (`identity.md`, `preferences.md`, `workflows.md`, etc.)
- Required directories exist (`core/`, `conversations/`)
- Required root files exist (`README.md`, `context-update.md`)
- Core files have valid YAML frontmatter
- Conversations directory has `README.md`

**Exit Codes:**
- `0` - Validation passed
- `1` - Validation failed (errors printed to stderr)

### `validate_transcript_metadata.py`

Validates conversation transcript metadata and checks for forbidden patterns (secrets, API keys).

**Usage:**
```bash
python executions/tools/context_validator/validate_transcript_metadata.py [project-root]
```

**Checks:**
- Transcripts have required frontmatter (`session_id`, `timestamp`, `participants`)
- No obvious secrets/API keys in transcripts (common patterns)
- Redaction markers are present when needed

**Forbidden Patterns Detected:**
- OpenAI API keys (`sk-...`)
- AWS access keys (`AKIA...`)
- GitHub tokens (`ghp_...`)
- Slack tokens (`xox...`)
- Bearer tokens
- Passwords (simple heuristic)
- Private keys

**Exit Codes:**
- `0` - Validation passed
- `1` - Validation failed (errors printed to stderr)

## Integration

These tools are integrated into:
- `scripts/validate_scaffold.py` - Scaffold validation
- Pre-promotion validation workflow
- CI/CD pipelines (if applicable)

## Dependencies

- Python 3.12+
- `pyyaml` (for frontmatter parsing)

## Notes

- These tools are **deterministic** - they check structure and patterns, not content meaning
- Secret detection uses heuristics - not foolproof, but catches common mistakes
- Transcripts should be redacted before creation (see `.context/conversations/README.md`)

