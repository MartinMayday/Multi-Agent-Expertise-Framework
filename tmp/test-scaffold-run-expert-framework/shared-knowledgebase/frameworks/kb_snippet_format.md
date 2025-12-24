# KB Snippet Format Standard

## Canonical Format

All KB snippets should follow this structure:

```markdown
---
id: unique-snippet-id
title: Snippet Title
source_type: official-doc|partial-doc|conversation-synthesis
source_url: https://example.com/docs
confidence: high|medium|low
tags: [tag1, tag2, tag3]
---

## Summary
Brief summary of the knowledge.

## Verified Facts
- Fact 1
- Fact 2

## Non-Facts / Open Questions
- Unknown 1
- Unknown 2

## Implications
What this means for design/implementation.

## Last Reviewed
YYYY-MM-DD
```

## Why This Format Works
- Frontmatter → retrieval + filtering
- Verified vs Non-Facts → hallucination control
- Implications → design handoff without assumptions
