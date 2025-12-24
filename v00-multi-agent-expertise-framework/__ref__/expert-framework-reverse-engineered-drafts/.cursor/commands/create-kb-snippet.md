# Create KB Snippet

Generate a knowledge base snippet in the standard format with proper source attribution.

## Action

Create a new KB snippet following the format in `shared-knowledgebase/frameworks/kb_snippet_format.md`.

## Required Information

1. **Source**: Where did this knowledge come from?
   - Official documentation URL
   - Conversation synthesis
   - Execution results

2. **Content**:
   - Summary
   - Verified Facts (what we know for certain)
   - Non-Facts / Open Questions (what we don't know or are uncertain about)
   - Implications (what this means for design/implementation)

3. **Metadata**:
   - Unique ID
   - Title
   - Source type (official-doc|partial-doc|conversation-synthesis)
   - Source URL (if applicable)
   - Confidence level (high|medium|low)
   - Tags for retrieval

## Output Location

Write to `review-approval/` first, then promote to `shared-knowledgebase/snippets/` after approval.

## Format Template

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

## Notes

- Check `shared-knowledgebase/manifest.md` first to avoid duplicates
- All facts must have source attribution
- Use appropriate confidence levels (don't overstate certainty)

