---
# -----------------------------------------------------------------------------
# HYBRID SEARCH PROTOCOL: AGENT INSTRUCTIONS
# -----------------------------------------------------------------------------
# 1. BM25: Optimize 'keywords' for exact term matching and domain specificity.
# 2. VECTOR: Optimize 'summary' & 'context_snippet' for dense semantic overlap.
# 3. RRF: Use 'rrf_anchors' to bridge terminology gaps (e.g., "K8s" vs "Kubernetes").
# 4. FILTER: Strict adherence to 'complexity', 'audience', and 'category' enums.
# -----------------------------------------------------------------------------

title: "{{TITLE_DESCRIPTIVE_AND_UNIQUE}}"
# CONSTRAINT: Must be < 60 chars, sentence case, unique across corpus.

filename: "{{FILENAME}}"

complexity: "{{ENUM: beginner | intermediate | advanced}}"
# HEURISTIC: 'advanced' implies assumes deep prior knowledge, 'beginner' explains basics.

audience: "{{ENUM: backend-engineers | data-scientists | devops-engineers | product-managers}}"
# HEURISTIC: Who acts on this information?

category: "{{ENUM: Knowledge Base | Instruction Stack | Design System | UX Patterns | Logic Flow | Security Heuristics}}"

keywords:
  # BM25 OPTIMIZATION: 12-20 high-signal terms.
  # INCLUDE: Specific libraries (e.g., 'pydantic'), error codes, acronyms, and synonyms.
  # AVOID: Generic terms like 'code', 'file', 'programming'.
  - "{{KEYWORD_1_PRIMARY_TOPIC}}"
  - "{{KEYWORD_2_SECONDARY_TOPIC}}"
  - "{{KEYWORD_3_SYNONYM}}"
  - "{{KEYWORD_4_ACRONYM_EXPANSION}}"
  - "{{KEYWORD_5_SPECIFIC_LIBRARY_OR_TOOL}}"
  # ... continue to ~15 keywords

tags:
  # TAXONOMY: 4-6 broad conceptual tags for faceting.
  - "{{TAG_1_DOMAIN}}"      # e.g., "observability"
  - "{{TAG_2_TECH_STACK}}"  # e.g., "python"
  - "{{TAG_3_PATTERN}}"     # e.g., "factory-pattern"

summary: |
  {{SEMANTIC_DENSE_VECTOR_SUMMARY}}
  # INSTRUCTION: Write a 50-80 word summary optimized for embeddings.
  # FOCUS: What problem does this solve? What is the core mechanism?
  # AVOID: "This file contains..." or conversational filler.

rrf_anchors:
  # RECIPROCAL RANK FUSION BRIDGES:
  # Terms that link this doc to queries using different vocabulary.
  - "{{FILENAME_STEM}}"
  - "{{CONCEPTUAL_ANCHOR_1}}" # e.g., "container-orchestration" for "k8s"
  - "{{CONCEPTUAL_ANCHOR_2}}" # e.g., "load-balancer" for "traefik"

context_snippet: |
  [MANDATORY HEURISTICS]
  {{CONTEXTUAL_RETRIEVAL_BLOCK}}
  # INSTRUCTION: 120-250 words situating this file in the broader system.
  # ANSWER: When should an agent retrieve this? What distinct rules does it enforce?
  # SOURCE: Extract specific constraints, configuration defaults, and architectural decisions.

  [NEGATIVE CONSTRAINTS]
  {{ANTI_PATTERNS_BLOCK}}
  # INSTRUCTION: What patterns are explicitly forbidden or replaced by this doc?
---
