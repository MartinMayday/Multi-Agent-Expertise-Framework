# Refactor Context Generator: Mission-Compliant Multi-Layer Progressive Context Loading

## Objective

Transform the context generator from a simple file-listing tool to a **mission-compliant progressive context loader** that generates YAML frontmatter-driven CLAUDE.md files with:

- **3-4 layer protocol** (L1: Summary, L2: Structured YAML, L3: Rich details, L4: Raw references)
- **Semantic retrieval metadata** (keywords, chunk_type, when_to_load conditions)
- **Hybrid search support** (BM25 terms, semantic hints, RRF ranking signals, RAGAS metadata)
- **On-demand context loading** based on agent intent/classification

---

## Architecture Overview

### Layer Structure (Progressive Loading)

| Layer | Purpose | Format | When Used |
| --- | --- | --- | --- |
| **L1** | Quick index/summary | Plain text, frontmatter headers | Initial folder discovery |
| **L2** | Structured blocks | YAML with metadata | Detailed file exploration |
| **L3** | Rich context | Full summaries, dependency maps | In-depth context window |
| **L4** | Raw references | File content links, full text pointers | Complete reference when needed |

### Multi-Component Architecture

```
context_generator/
├── core/
│   ├── scanner.py          # [EXISTING] File discovery
│   ├── extractor.py        # [EXISTING] Symbol extraction
│   └── analyzer.py         # [EXISTING] Dependency analysis
│
├── metadata/
│   ├── __init__.py         # [NEW] Metadata generation package
│   ├── frontmatter_builder.py  # [NEW] YAML frontmatter construction
│   ├── keyword_extractor.py    # [NEW] Semantic keyword generation
│   ├── intent_classifier.py    # [NEW] chunk_type & intent classification
│   └── search_metadata.py      # [NEW] BM25, semantic hints, RAGAS prep
│
├── retrieval/
│   ├── __init__.py         # [NEW] Retrieval strategy package
│   ├── search_strategies.py    # [NEW] RRF, BM25, semantic ranking
│   └── ragas_scorer.py         # [NEW] RAGAS metric preparation (optional)
│
├── protocols/
│   ├── __init__.py         # [NEW] Progressive loading protocols
│   └── layer_manager.py    # [NEW] L1-L4 layer orchestration
│
├── templates/
│   ├── claude_l1_index.jinja2    # [NEW] Layer 1: Quick index
│   ├── claude_l2_blocks.jinja2   # [NEW] Layer 2: YAML blocks
│   ├── claude_l3_detail.jinja2   # [NEW] Layer 3: Rich context
│   ├── claude_l4_refs.jinja2     # [NEW] Layer 4: Raw references
│   └── claude_md.jinja2          # [MODIFY] Updated main template
│
├── executions/
│   ├── llm_client.py       # [EXISTING]
│   ├── directive_loader.py # [EXISTING]
│   ├── executors.py        # [MODIFY] Extend for frontmatter output
│   └── metadata_executor.py    # [NEW] LLM-enhanced metadata generation
│
└── generator.py            # [REFACTOR] Multi-layer orchestration
```

---

## New Classes & Responsibilities

### 1. `metadata/frontmatter_builder.py`

**Class:** `FrontmatterBuilder`

Generates YAML frontmatter for each file with:

```yaml
---
id: {file-id}
path: {relative-path}
tokens: {estimated}
chunk_type: {contract|methodology|architecture|execution|reference}
keywords:
  - {semantic-keyword-1}
  - {bm25-term-1}
priority: {high|medium|low}
summary: |
  {1-2 line rich summary}
when_to_load: |
  - Condition 1
  - Condition 2
retrieval_triggers:
  - "{semantic-phrase}"
dependencies:
  - {other-file-ids}
search_hints:
  bm25_terms: [term1, term2, ...]
  semantic_signals: [signal1, signal2, ...]
  ragas_candidate: true
---
```

**Methods:**

- `build_frontmatter(file: ScannedFile, symbols: FileSymbols, analysis_result: AnalysisResult) → str`
- `classify_chunk_type(content: str, file_path: str) → str`
- `generate_keywords(symbols, content, file_type) → list[str]`
- `prioritize_file(file_stats, dependency_score) → str`

### 2. `metadata/keyword_extractor.py`

**Class:** `KeywordExtractor`

Extracts searchable terms using multiple strategies:

```python
def extract_keywords(
    file_content: str,
    symbols: FileSymbols,
    file_type: str
) -> dict:
    return {
        "semantic": [...],      # LLM-generated semantic terms
        "bm25": [...],         # TF-IDF important terms
        "entities": [...],     # Named entity extraction
        "topics": [...]        # Topic model clusters
    }
```

**Strategies:**

- **Semantic**: LLM-based intent keywords (via LLMClient + directive)
- **BM25**: TF-IDF weighted term extraction (sklearn/gensim)
- **Entities**: Simple regex for class/function names from symbols
- **Topics**: Module-level categorization (config, utils, core, etc.)

### 3. `metadata/intent_classifier.py`

**Class:** `IntentClassifier`

Classifies file intent and generates `when_to_load` conditions:

```python
def classify(file_content: str, symbols: FileSymbols, path: str) -> IntentResult:
    return IntentResult(
        chunk_type: "methodology",  # contract|methodology|architecture|execution|reference
        when_to_load: [
            "Agent needs framework reference",
            "Validating behavior against rules",
        ],
        retrieval_triggers: [
            "prompt engineering",
            "refinement framework"
        ]
    )
```

**Classification Logic:**

- **contract**: Contains rules, guardrails, validation, constraints
- **methodology**: Contains frameworks, patterns, procedures, templates
- **architecture**: Contains system design, components, dependencies, interfaces
- **execution**: Contains implementation, code, workflows, runbooks
- **reference**: Contains definitions, glossaries, lookups, index

### 4. `metadata/search_metadata.py`

**Class:** `SearchMetadata`

Generates search-friendly metadata for hybrid retrieval:

```python
def generate(file_entry: FileEntry) -> SearchHints:
    return {
        "bm25_terms": [...],
        "semantic_signals": [...],
        "lexical_variants": [...],
        "ragas_relevance": float,  # 0.0-1.0 confidence for RAGAS
        "rrf_rank": int,           # For Reciprocal Rank Fusion
    }
```

### 5. `retrieval/search_strategies.py`

**Class:** `HybridSearchStrategy`

Implements multi-strategy retrieval ranking:

```python
def rank_files(
    query: str,
    all_files: list[FileEntry],
    weights: dict  # {bm25: 0.3, semantic: 0.4, lexical: 0.2, keywords: 0.1}
) -> list[RankedFile]:
    # RRF (Reciprocal Rank Fusion) combination
    # BM25 scoring of keywords
    # Semantic similarity (if embeddings available)
    # Lexical matching (exact term matches)
    return ranked
```

### 6. `protocols/layer_manager.py`

**Class:** `LayerManager`

Orchestrates multi-layer progressive loading:

```python
class LayerManager:
    def generate_layers(
        folder: ScannedFolder,
        llm_client: BaseLLMClient
    ) -> MultiLayerOutput:
        # L1: Fast index (names + keywords)
        # L2: Structured YAML (frontmatter + summaries)
        # L3: Rich context (full summaries + dependency maps)
        # L4: Raw references (file links, byte ranges)
        return MultiLayerOutput(l1, l2, l3, l4)
```

---

## Modified Existing Files

### `generator.py` - Refactor to Multi-Layer Orchestration

**Current Flow:**

```
ClaudeMdGenerator.generate_for_folder()
  → scan files
  → extract symbols
  → call LLM for descriptions
  → render template
```

**New Flow:**

```
ClaudeMdGenerator.generate_for_folder()
  → [L0] Scan files & extract metadata
  → [L1] Generate quick index (FileScanner + keywords)
  → [L2] Build structured YAML (FrontmatterBuilder + IntentClassifier)
  → [L3] Generate rich context (LLM executors + summaries)
  → [L4] Create references (raw content pointers)
  → [LAYER_MANAGER] Combine into multi-layer output
  → render LayerManager template
```

**New Dataclasses:**

```python
@dataclass
class FileEntryL2:
    name: str
    frontmatter: dict  # YAML parsed
    keywords: list[str]
    chunk_type: str
    when_to_load: list[str]
    retrieval_triggers: list[str]
    description: str

@dataclass
class MultiLayerOutput:
    layer_1: str  # Quick index markdown
    layer_2: str  # YAML frontmatter blocks
    layer_3: str  # Rich context + dependencies
    layer_4: str  # Raw references
    combined_claude_md: str  # Full output
```

### `executions/executors.py` - Extend for Frontmatter Output

Add new executor:

```python
class MetadataExecutor(BaseExecutor):
    """Generates YAML frontmatter metadata via LLM."""
    
    def execute(
        file_content: str,
        symbols: FileSymbols
    ) -> MetadataResult:
        # Use LLM + directive to generate:
        # - semantic keywords
        # - when_to_load conditions
        # - retrieval_triggers
        # - chunk_type classification
        pass
```

### `templates/claude_md.jinja2` - Add Layer Selection

```jinja2
{# Layer 1: Quick Index #}
{% if include_layer_1 %}
## L1: Quick Index
{{ layer_1_content }}
{% endif %}

{# Layer 2: Structured YAML #}
{% if include_layer_2 %}
## L2: File Metadata
{% for file in files_l2 %}
{{ file.frontmatter_block }}
{% endfor %}
{% endif %}

{# Layer 3: Rich Context #}
{% if include_layer_3 %}
## L3: Context Window
{{ layer_3_content }}
{% endif %}

{# Layer 4: References #}
{% if include_layer_4 %}
## L4: Raw References
{{ layer_4_content }}
{% endif %}
```

---

## New Directives (YAML SOPs)

Create in `context_generator/directives/`:

### `generate_keywords.yaml`

```yaml
name: generate_keywords
template: |
  TASK: Extract searchable keywords from file metadata.
  
  FILE: {filename}
  SYMBOLS: {symbol_list}
  CONTENT_PREVIEW: {first_200_chars}
  
  REQUIREMENTS:
  - 3-5 semantic keywords (intent, purpose, pattern)
  - 2-3 BM25 terms (most distinctive words)
  - Return as YAML list
```

### `classify_intent.yaml`

```yaml
name: classify_intent
template: |
  TASK: Classify file intent and when to load.
  
  FILE: {filename}
  PATH: {full_path}
  FIRST_LINES: {first_100_lines}
  
  CHUNK TYPES: contract|methodology|architecture|execution|reference
  
  RETURN:
  chunk_type: [one of above]
  when_to_load:
    - [condition 1]
    - [condition 2]
  retrieval_triggers:
    - "[trigger phrase 1]"
    - "[trigger phrase 2]"
```

---

## Implementation Sequence

### Phase 1: Foundation (Metadata Generation)

1. Create `metadata/frontmatter_builder.py` with YAML construction
2. Create `metadata/keyword_extractor.py` with BM25 + semantic strategies
3. Create `metadata/intent_classifier.py` with rule-based classification
4. Add new directives (`generate_keywords.yaml`, `classify_intent.yaml`)

### Phase 2: Retrieval & Ranking

5. Create `retrieval/search_strategies.py` with RRF + hybrid ranking
6. Create `metadata/search_metadata.py` for search hints
7. Add RAGAS preparation (optional, minimal)

### Phase 3: Layer Protocol

8. Create `protocols/layer_manager.py` to orchestrate L1-L4
9. Create layer-specific templates (L1-L4)

### Phase 4: Integration

10. Refactor `generator.py` to use LayerManager
11. Update `templates/claude_md.jinja2` with layer support
12. Extend `executors.py` with MetadataExecutor
13. Update CLI to accept `--layers` flag (default: L1+L2+L3)

---

## CLI Changes

### New Arguments:

```bash
python -m context_generator /path \
  --layers "1,2,3"           # Which layers to include (default: 1,2,3)
  --search-weights "bm25=0.3,semantic=0.4,keywords=0.2"  # RRF weights
  --chunk-types "contract,methodology"  # Filter by type (optional)
  --include-ragas            # Add RAGAS metadata (optional)
```

### Output Structure:

```
/path/to/project/
├── CLAUDE.md               # Combined multi-layer output
├── .claude/
│   ├── layer_1_index.md    # L1 quick index
│   ├── layer_2_blocks.yaml # L2 structured YAML
│   ├── layer_3_context.md  # L3 rich context
│   └── layer_4_refs.md     # L4 raw references
```

---

## Dependencies & Constraints

### New Python Dependencies:

- `scikit-learn>=1.0` (BM25/TF-IDF)
- `nltk>=3.8` (tokenization, stopwords for keyword extraction)
- No new external LLM requirements (uses existing LLMClient)

### Backward Compatibility:

- Existing `ClaudeMdGenerator` interface preserved (layer support added)
- Existing CLAUDE.md output still generated (enhanced with frontmatter)
- `.env` configuration compatible (new optional flags)

### Performance Constraints:

- Keyword extraction: &lt;1s per file (local algorithms)
- Intent classification: Use local rules first, LLM only if ambiguous
- Layer generation sequential (L1→L2→L3→L4) to avoid redundant LLM calls

---

## Verification & Definition of Done

| Step | Target | Success Criteria |
| --- | --- | --- |
| 1 | Frontmatter generation | File contains valid YAML frontmatter with all required fields |
| 2 | Keyword extraction | ≥3 semantic + ≥2 BM25 keywords per file |
| 3 | Intent classification | chunk_type assigned, when_to_load non-empty |
| 4 | Layer generation | All 4 layers output correctly |
| 5 | Search metadata | RRF signals present, RAGAS prep optional but available |
| 6 | Template rendering | CLAUDE.md valid markdown with layer sections |
| 7 | CLI integration | `--layers` flag works, `.claude/` directory created |
| 8 | Mission compliance | Output matches agentic_index.txt frontmatter format |

---

## Risks & Mitigation

| Risk | Mitigation |
| --- | --- |
| LLM cost explosion (keyword + intent LLM calls) | Use local rules first, LLM only for ambiguous files |
| Low keyword quality | Combine BM25 + semantic + entity extraction; human review fallback |
| Inconsistent chunk_type classification | Hard rules + LLM validation; AGENTS.md guidance |
| Performance degradation | Layer generation optional; cache intermediate results |

---

## Next Steps After Approval

1. Implement Phase 1 (Metadata generation) with comprehensive tests
2. Create example output showing frontmatter format matching mission requirements
3. Validate against `agentic_index.txt` format compliance
4. Integration testing with real codebases (context_generator itself, test projects)
5. Performance profiling and optimization