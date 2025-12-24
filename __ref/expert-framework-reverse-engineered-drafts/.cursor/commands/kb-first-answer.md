# KB-First Answer

Enforce KB gate before producing any response.

## Action

1. Read `shared-knowledgebase/manifest.md`
2. Read relevant agent KB manifest (`kb_<agent>-manifest.md`)
3. Declare `KB_STATUS`: `sufficient`, `partial`, or `insufficient`
4. If insufficient: STOP, document what's missing, ask user for approval to research
5. After research: Generate KB snippets in standard format
6. Only then produce the response, citing KB snippet IDs

## KB Status Declaration

**Format**:
```
KB_STATUS: sufficient|partial|insufficient

If partial or insufficient:
- Missing information: [list what's needed]
- Why it blocks progress: [explanation]
- Approval needed: yes|no
```

## KB Snippet Format

See `shared-knowledgebase/frameworks/kb_snippet_format.md` for the standard format.

Required fields:
- Frontmatter: id, title, source_type, source_url, confidence, tags
- Verified Facts section
- Non-Facts / Open Questions section
- Implications section

## Enforcement

- No response without KB_STATUS declaration
- No unsourced claims
- All facts must trace to KB snippets or documentation

