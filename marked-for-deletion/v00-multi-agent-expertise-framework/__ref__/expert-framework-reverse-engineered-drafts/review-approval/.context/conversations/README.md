# Conversation Transcripts

This directory contains **full conversation transcripts** of all AI/LLM interactions with this repository.

## Purpose

Transcripts serve multiple purposes:
- **History**: Complete record of what was discussed
- **Learnings**: Patterns, failures, successful approaches
- **Rollback**: Understanding what changed and why
- **Evaluation**: Analyzing agent performance over time
- **Context continuity**: Never start from scratch

## Naming Convention

Transcript files use this format:
```
[session-id]-[timestamp].md
```

Example:
```
sess-20241223-143512-abc123.md
```

Where:
- `sess-` = prefix indicating session transcript
- `20241223` = date (YYYYMMDD)
- `143512` = time (HHMMSS)
- `abc123` = unique identifier (optional, for collisions)

## File Structure

Each transcript file must include:

### Frontmatter (YAML)

```yaml
---
session_id: sess-20241223-143512-abc123
timestamp: 2024-12-23T14:35:12Z
participants:
  - agent: metagpt
    model: claude-sonnet-4.5
  - user: [user-identifier]
tools_used:
  - read_file
  - write
  - run_terminal_cmd
redactions:
  - line: 42
    reason: API key detected
  - line: 156
    reason: Personal information
---
```

### Content

Full conversation transcript including:
- User messages
- Agent responses
- Tool calls and outputs
- Error messages
- System reminders

## Redaction Rules

**CRITICAL**: Never include secrets in transcripts.

### What to Redact

- API keys, tokens, passwords
- Personal information (unless explicitly about repo stakeholders)
- Sensitive configuration values
- Credentials or authentication data

### How to Redact

Use markers in the transcript:
```
[REDACTED: API key detected]
[REDACTED: Personal information]
[REDACTED: Sensitive configuration]
```

And document in frontmatter:
```yaml
redactions:
  - line: 42
    reason: API key detected
```

## Append-Only Policy

**Transcripts are append-only** — once created, never modify:
- ✅ Create new transcript after each session
- ❌ Never edit existing transcripts
- ❌ Never delete transcripts (archive if needed)

## Loading Transcripts

Transcripts are **excluded from default context** (via `.cursorignore`) because they're large.

To load a specific transcript:
1. Identify the session ID or date
2. Load the specific transcript file on demand
3. Don't load all transcripts — only what's needed

## Integration with Session Tracking

- Transcripts complement `planning/WORKSESSION_STATE.md`
- Transcripts complement `.context/core/session.md`
- Transcripts provide full detail; session files provide summaries

## Storage Considerations

- Transcripts can grow large quickly
- Consider periodic archival of old transcripts
- Keep active transcripts (last 30 days) in this directory
- Archive older transcripts to `marked-for-deletion/` or external storage

## Template

See `transcript-template.md` for the standard transcript format.

