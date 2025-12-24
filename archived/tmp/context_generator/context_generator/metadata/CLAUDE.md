# metadata

## Purpose
metadata - no public symbols; no public symbols; class FrontmatterMetadata, +1 classes; class IntentResult, +1 

## File Metadata (YAML Frontmatter)

### CLAUDE.md
---
id: CLAUDE
path: CLAUDE.md
tokens: 1406
chunk_type: execution
keywords:
- execution
- priority
- frontmattermetadata
- intentresult
- 'metadata


  '
- class
- metadata
- claude
- workflow
priority: medium
summary: N/A
when_to_load:
- Agent needs implementation details
- Writing or debugging code
- Understanding workflow execution
retrieval_triggers:
- implementation details
- code execution
- workflow steps
- runbook procedures
search_hints:
  bm25_terms:
  - execution
  - priority
  - frontmattermetadata
  - intentresult
  - 'metadata


    '
  - class
  - metadata
  - claude
  - workflow
  semantic_signals: []
---

### __init__.py
---
id: __init__
path: __init__.py
tokens: 127
chunk_type: execution
keywords:
- init
- frontmatterbuilder
- keywordextractor
- intentclassifier
- import
priority: medium
summary: Metadata generation for progressive context loading.
when_to_load:
- Agent needs implementation details
- Writing or debugging code
- Understanding workflow execution
retrieval_triggers:
- implementation details
- code execution
- workflow steps
- runbook procedures
search_hints:
  bm25_terms:
  - init
  - frontmatterbuilder
  - keywordextractor
  - intentclassifier
  - import
  semantic_signals: []
---

### frontmatter_builder.py
---
id: frontmatter_builder
path: frontmatter_builder.py
tokens: 1241
chunk_type: execution
keywords:
- return
- __future__
- frontmatter
- list
- tokens
- builder
- class
- configuration
- annotations
priority: medium
summary: Build YAML frontmatter for file metadata.
when_to_load:
- Agent needs implementation details
- Writing or debugging code
- Understanding workflow execution
retrieval_triggers:
- implementation details
- code execution
- workflow steps
- runbook procedures
search_hints:
  bm25_terms:
  - return
  - __future__
  - frontmatter
  - list
  - tokens
  - builder
  - class
  - configuration
  - annotations
  semantic_signals: []
---

### intent_classifier.py
---
id: intent_classifier
path: intent_classifier.py
tokens: 1560
chunk_type: methodology
keywords:
- chunk_type
- intent
- framework
- class
- intentclassifier
- contract
- content
- logger
- self
- classifier
priority: medium
summary: Classify file intent and generate when_to_load conditions.
when_to_load:
- Agent needs methodology guidance for task
- Implementing best practices or patterns
- Refining approach or methodology
retrieval_triggers:
- framework reference
- best practices
- methodology guidance
- pattern implementation
search_hints:
  bm25_terms:
  - chunk_type
  - intent
  - framework
  - class
  - intentclassifier
  - contract
  - content
  - logger
  - self
  - classifier
  semantic_signals: []
---

### keyword_extractor.py
---
id: keyword_extractor
path: keyword_extractor.py
tokens: 1269
chunk_type: execution
keywords:
- list
- from
- extractor
- keywordextractor
- class
- content
- configuration
- keyword
- self
priority: medium
summary: Extract searchable keywords using multiple strategies.
when_to_load:
- Agent needs implementation details
- Writing or debugging code
- Understanding workflow execution
retrieval_triggers:
- implementation details
- code execution
- workflow steps
- runbook procedures
search_hints:
  bm25_terms:
  - list
  - from
  - extractor
  - keywordextractor
  - class
  - content
  - configuration
  - keyword
  - self
  semantic_signals: []
---

### search_metadata.py
---
id: search_metadata
path: search_metadata.py
tokens: 3409
chunk_type: execution
keywords:
- __future__
- list
- file
- keywords
- metadata
- search
- class
- configuration
- annotations
priority: high
summary: Search metadata and RAGAS preparation for retrieval evaluation.
when_to_load:
- Agent needs implementation details
- Writing or debugging code
- Understanding workflow execution
retrieval_triggers:
- implementation details
- code execution
- workflow steps
- runbook procedures
search_hints:
  bm25_terms:
  - __future__
  - list
  - file
  - keywords
  - metadata
  - search
  - class
  - configuration
  - annotations
  semantic_signals: []
---


## Files
| File | Symbols | Tokens | Chunk Type | Keywords | RAGAS | Retrieval | Description |
|------|---------|--------|------------|----------|-------|-----------|-------------|
| `CLAUDE.md` | no public symbols | ~1406 | execution | execution, priority, frontmattermetadata, intentresult, metadata

, class, metadata, claude, workflow | 0.93 | 0.0163 | N/A |
| `__init__.py` | no public symbols | ~127 | execution | init, frontmatterbuilder, keywordextractor, intentclassifier, import | 0.76 | 0.0160 | Metadata generation for progressive context loading. |
| `frontmatter_builder.py` | class FrontmatterMetadata, +1 classes | ~1241 | execution | return, __future__, frontmatter, list, tokens, builder, class, configuration, annotations | 0.93 | 0.0159 | Build YAML frontmatter for file metadata. |
| `intent_classifier.py` | class IntentResult, +1 classes | ~1560 | methodology | chunk_type, intent, framework, class, intentclassifier, contract, content, logger, self, classifier | 0.95 | 0.0158 | Classify file intent and generate when_to_load conditions. |
| `keyword_extractor.py` | class KeywordResult, +1 classes | ~1269 | execution | list, from, extractor, keywordextractor, class, content, configuration, keyword, self | 0.93 | 0.0154 | Extract searchable keywords using multiple strategies. |
| `search_metadata.py` | class RAGASMetrics, +3 classes | ~3409 | execution | __future__, list, file, keywords, metadata, search, class, configuration, annotations | 0.93 | 0.0152 | Search metadata and RAGAS preparation for retrieval evaluation. |



