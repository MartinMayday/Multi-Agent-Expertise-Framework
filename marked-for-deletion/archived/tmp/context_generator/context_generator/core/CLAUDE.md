# core

## Purpose
core - no public symbols; no public symbols; class Dependency, +2 classes; class Symbol, +2 classes; class 

## File Metadata (YAML Frontmatter)

### CLAUDE.md
---
id: CLAUDE
path: CLAUDE.md
tokens: 157
chunk_type: architecture
keywords:
- scannedfile
- core
- symbol
- architecture
- class
- classes
- claude
- graph
- dependency
priority: medium
summary: N/A
when_to_load:
- Agent needs system design context
- Understanding component relationships
- Analyzing architectural implications
retrieval_triggers:
- system design
- component interaction
- architectural patterns
- dependency mapping
search_hints:
  bm25_terms:
  - scannedfile
  - core
  - symbol
  - architecture
  - class
  - classes
  - claude
  - graph
  - dependency
  semantic_signals: []
---

### __init__.py
---
id: __init__
path: __init__.py
tokens: 9
chunk_type: reference
keywords:
- core
- architecture
- static
- analysis
- init
priority: medium
summary: Core static analysis modules.
when_to_load:
- Agent needs lookup or definition
- Cross-referencing related concepts
- Validating against baseline
retrieval_triggers:
- definition lookup
- concept reference
- glossary entry
- index reference
search_hints:
  bm25_terms:
  - core
  - architecture
  - static
  - analysis
  - init
  semantic_signals: []
---

### analyzer.py
---
id: analyzer
path: analyzer.py
tokens: 1801
chunk_type: architecture
keywords:
- configuration
- __future__
- import
- folder
- class
- analyzer
- self
- path
- graph
priority: medium
summary: Dependency analyzer for import graph construction.
when_to_load:
- Agent needs system design context
- Understanding component relationships
- Analyzing architectural implications
retrieval_triggers:
- system design
- component interaction
- architectural patterns
- dependency mapping
search_hints:
  bm25_terms:
  - configuration
  - __future__
  - import
  - folder
  - class
  - analyzer
  - self
  - path
  - graph
  semantic_signals: []
---

### extractor.py
---
id: extractor
path: extractor.py
tokens: 2954
chunk_type: execution
keywords:
- configuration
- name
- __future__
- extractor
- logging
- self
- node
- annotations
- ast
priority: high
summary: Symbol extractor using tree-sitter for multi-language AST parsing.
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
  - configuration
  - name
  - __future__
  - extractor
  - logging
  - self
  - node
  - annotations
  semantic_signals: []
---

### scanner.py
---
id: scanner
path: scanner.py
tokens: 1868
chunk_type: methodology
keywords:
- configuration
- framework
- __future__
- logging
- self
- return
- scanner
- path
- annotations
- dataclasses
priority: medium
summary: File scanner with .gitignore support.
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
  - configuration
  - framework
  - __future__
  - logging
  - self
  - return
  - scanner
  - path
  - annotations
  - dataclasses
  semantic_signals: []
---


## Files
| File | Symbols | Tokens | Chunk Type | Keywords | Description |
|------|---------|--------|------------|----------|-------------|
| `CLAUDE.md` | no public symbols | ~157 | architecture | scannedfile, core, symbol, architecture, class, classes, claude, graph, dependency | N/A |
| `__init__.py` | no public symbols | ~9 | reference | core, architecture, static, analysis, init | Core static analysis modules. |
| `analyzer.py` | class Dependency, +2 classes | ~1801 | architecture | configuration, __future__, import, folder, class, analyzer, self, path, graph | Dependency analyzer for import graph construction. |
| `extractor.py` | class Symbol, +2 classes | ~2954 | execution | configuration, name, __future__, extractor, logging, self, node, annotations, ast | Symbol extractor using tree-sitter for multi-language AST parsing. |
| `scanner.py` | class ScannedFile, +2 classes | ~1868 | methodology | configuration, framework, __future__, logging, self, return, scanner, path, annotations, dataclasses | File scanner with .gitignore support. |



