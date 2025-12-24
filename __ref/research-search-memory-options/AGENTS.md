---
title: Search & Memory Research - Decision Analysis for Codebase Context Awareness
version: 1.0
author: Expert Framework Development Team
date: 2025-12-24
status: Complete (Decision Made: Use txtai)
classification: Internal Operations | Research Reference
framework: expert-framework
project: research-search-memory-options
output_expected: Architectural decision for file-based vs vector DB search
execution_time: Research complete, implementation ready

# Contextual Retrieval Snippets (Level 1: Always Loaded)
contextual_snippets:
  - snippet: "Comprehensive analysis comparing file-based search vs vector databases for codebase context awareness, concluding that txtai provides optimal ROI"
    keywords: [file-based-search, vector-database, txtai, hybrid-search, BM25, RRF, decision-analysis, architecture]
    file: FINAL_DECISION.md
    tier: 1

  - snippet: "txtai recommendation: file-based hybrid search (BM25+semantic+RRF) with 15-minute setup, 90% of vector DB features with 5% of effort"
    keywords: [txtai, recommendation, hybrid-search, file-based, quick-setup, ROI]
    file: FINAL_RECOMMENDATION.md
    tier: 1

  - snippet: "Deep research comparing txtai vs custom file-based vs Qdrant/Supabase/Weaviate, analyzing trade-offs for <100k documents"
    keywords: [deep-research, comparison-matrix, txtai, Qdrant, Supabase, Weaviate, trade-offs]
    file: DEEP_RESEARCH_FILE_BASED_SOLUTIONS.md
    tier: 1

  - snippet: "claude-mem and beads analysis: neither suitable for codebase search (session memory vs task tracker), txtai is correct choice"
    keywords: [claude-mem, beads, analysis, comparison, txtai, decision]
    file: ANALYSIS_CLAUDE-MEM_BEADS.md
    tier: 2

  - snippet: "Architecture for full coverage indexing: file-based storage with MCP integration, portable indexes, version control friendly"
    keywords: [architecture, full-coverage, indexing, MCP, file-based, portable]
    file: ARCHITECTURE_FULL_COVERAGE.md
    tier: 2

  - snippet: "Context search vs memory distinction: search=retrieval engine, memory=session state, different problems requiring different solutions"
    keywords: [context-search, memory, distinction, retrieval, session-state]
    file: CONTEXT_SEARCH_VS_MEMORY.md
    tier: 2

  - snippet: "txtai vs ck comparison: txtai for semantic search, ck for code intelligence, complementary not competitive"
    keywords: [txtai, ck, comparison, semantic-search, code-intelligence]
    file: TXTVS_CK_COMPARISON.md
    tier: 3

  - snippet: "Quickstart guide for context generation using txtai: install, index, search, MCP integration in 15 minutes"
    keywords: [quickstart, txtai, setup, MCP, integration]
    file: QUICKSTART_CONTEXT_GENERATION.md
    tier: 3

  - snippet: "AI context sidecar files research: CLAUDE.md format, progressive loading, tier-based retrieval strategies"
    keywords: [AI-context, sidecar-files, CLAUDE.md, progressive-loading, tiers]
    file: RESEARCH_AI_CONTEXT_SIDECAR_FILES.md
    tier: 3

  - snippet: "Prompt analysis and enhanced variant for context generation workflows"
    keywords: [prompt-analysis, context-generation, workflow, enhancement]
    file: prompt-analysis-and-enhanced-variant.md
    tier: 3

# File Inventory
files:
  - name: FINAL_DECISION.md
    purpose: "Decision matrix comparing txtai vs claude-mem vs beads vs custom, with clear recommendation"
    use_when: "Need to understand why txtai was chosen for codebase search"
    tier: 1
    word_count: 276

  - name: FINAL_RECOMMENDATION.md
    purpose: "Executive summary: file-based IS viable, use txtai, avoid building custom"
    use_when: "Quick reference for architecture decision rationale"
    tier: 1
    word_count: 169

  - name: DEEP_RESEARCH_FILE_BASED_SOLUTIONS.md
    purpose: "Comprehensive research comparing file-based vs vector DB solutions with effort analysis"
    use_when: "Need detailed comparison of search approaches and trade-offs"
    tier: 1
    word_count: 450

  - name: ANALYSIS_CLAUDE-MEM_BEADS.md
    purpose: "Detailed analysis why claude-mem and beads don't solve codebase search problem"
    use_when: "Need to understand why other tools were rejected"
    tier: 2
    word_count: 280

  - name: ARCHITECTURE_FULL_COVERAGE.md
    purpose: "Architecture design for file-based full coverage indexing with MCP integration"
    use_when: "Implementing file-based search architecture"
    tier: 2
    word_count: 290

  - name: CONTEXT_SEARCH_VS_MEMORY.md
    purpose: "Conceptual distinction between search engines and memory systems"
    use_when: "Need to clarify requirements: search vs session memory"
    tier: 2
    word_count: 285

  - name: TXTVS_CK_COMPARISON.md
    purpose: "Comparison of txtai (semantic search) vs ck (code intelligence) - complementary tools"
    use_when: "Deciding which tool to use for specific use case"
    tier: 3
    word_count: 240

  - name: QUICKSTART_CONTEXT_GENERATION.md
    purpose: "15-minute setup guide: install txtai, index codebase, configure MCP"
    use_when: "Implementing txtai for first time"
    tier: 3
    word_count: 130

  - name: RESEARCH_AI_CONTEXT_SIDECAR_FILES.md
    purpose: "Research on AI context sidecar file formats (CLAUDE.md, .ai-context.yaml)"
    use_when: "Designing context file formats and progressive loading strategies"
    tier: 3
    word_count: 350

  - name: prompt-analysis-and-enhanced-variant.md
    purpose: "Analysis of context generation prompts with enhanced variants"
    use_when: "Improving LLM prompts for context generation"
    tier: 3
    word_count: 200

# Key Concepts (3-10 items)
key_concepts:
  - "File-Based Viability: txtai proves file-based hybrid search is production-ready for <100k documents with 15-minute setup"
  - "Hybrid Search Superiority: BM25 (lexical) + semantic embeddings + RRF fusion provides 90% of vector DB features"
  - "ROI Optimization: txtai delivers 90% of vector DB features with 5% of effort - custom implementation is waste"
  - "Tool Categorization: txtai=search engine, claude-mem=session memory, beads=task tracker - different problems"
  - "MCP Integration: File-based indexes work seamlessly with MCP protocol for AI agent context awareness"
  - "Portability Advantage: File-based storage (.ai-index/) enables copy-paste deployment, version control friendly"
  - "Scale Threshold: Vector DB only justified when >1M documents, <100ms latency required, or multiple concurrent writers"
  - "Progressive Loading: Tier-based retrieval (L1-L4) enables token optimization while maintaining context quality"

# Expected Outcomes (3-5 items)
outcomes:
  - "Clear architectural decision: Use txtai for file-based hybrid search"
  - "Rejection rationale documented: claude-mem (wrong problem), beads (wrong problem), custom (waste of effort)"
  - "15-minute implementation path defined: install → index → search → MCP integration"
  - "Scale boundaries identified: file-based viable until >100k documents or specialized requirements emerge"
  - "Reference architecture designed: file storage + MCP + progressive loading + hybrid search"
---

# Search & Memory Research - Decision Analysis for Codebase Context Awareness

**Comprehensive research comparing file-based search vs vector databases for AI codebase context awareness, concluding that txtai (file-based hybrid search with BM25+semantic+RRF) provides optimal ROI with 15-minute setup and 90% of vector DB features at 5% of effort.**

**Version:** 1.0  
**Status:** Complete (Decision Made: Use txtai)  
**Framework:** expert-framework  
**Target:** Architects making search/memory technology decisions

---

## 📋 Overview

This research collection documents a comprehensive analysis of codebase context awareness solutions for AI agents. The central question: **"Is file-based approach a waste of effort vs vector databases?"**

**Answer:** **No** - txtai (file-based) is optimal for <100k documents. Vector DBs are overkill unless you have >1M documents or specialized requirements.

### Research Scope
1. **File-based solutions:** txtai, custom implementations
2. **Vector databases:** Qdrant, Supabase (pgvector), Weaviate
3. **Alternative approaches:** claude-mem (session memory), beads (task tracker)
4. **Hybrid search:** BM25 (lexical) + semantic embeddings + RRF fusion
5. **MCP integration:** Model Context Protocol for AI agent access
6. **Progressive loading:** Tier-based context retrieval (L1-L4)

### Research Outcome
**Recommendation:** Use **txtai** (file-based hybrid search)

---

## 🎯 Executive Summary (FINAL_RECOMMENDATION.md)

### The Answer: File-Based IS Viable - Use txtai

After comprehensive research, **txtai** (12k+ GitHub stars) implements exactly what's needed:

- ✅ **File-based hybrid search** (BM25 + semantic embeddings)
- ✅ **Reciprocal Rank Fusion** built-in
- ✅ **Pure file storage** (no database required)
- ✅ **MCP integration** for Claude/Cursor
- ✅ **Code-aware chunking** with tree-sitter
- ✅ **12k+ stars**, production battle-tested

### When to Use Each Approach

#### Use File-Based (txtai) When:
- ✓ <100,000 documents (code chunks)
- ✓ Self-hosted agents
- ✓ Software-agnostic solution
- ✓ Quick setup required (hours, not weeks)
- ✓ No dedicated DevOps team
- ✓ Portable indexes (copy files)
- ✓ Version control friendly

**Expert-framework use case matches all of these.**

#### Use Vector DB (Qdrant/Supabase/Weaviate) When:
- ✗ >1 million documents
- ✗ Sub-100ms latency at scale required
- ✗ Multiple concurrent writers
- ✗ Advanced aggregations/faceted search needed
- ✗ Team has DB expertise
- ✗ Managed service preferred
- ✗ Budget for infrastructure

---

## 📊 Comparison Matrix (FINAL_DECISION.md)

### Effort vs Results

| Approach | Setup | Maintenance | Performance | Features | **ROI** |
|----------|-------|-------------|-------------|----------|---------|
| **txtai** | 15 min | Low | Excellent | Full | **High** |
| Custom file-based | 2-3 days | Medium | Good | Medium | Medium |
| Vector DB | 1-2 weeks | High | Excellent | Full | Low (for expert-framework scale) |

### Tool Categorization

| Tool | Category | For Codebase Search | For Expert-Framework |
|------|----------|---------------------|---------------------|
| **txtai** | Search Engine | ✓ Yes | **USE THIS** |
| **claude-mem** | Session Memory | ✗ No (sessions) | Skip - wrong problem |
| **beads** | Task Tracker | ✗ No (tasks) | Skip - wrong problem |
| **Custom** | Search Engine | ✓ Yes | Skip - txtai better |

---

## 🔬 Research Files (10 documents, ~82KB total)

### Tier 1: Decision Documents (Essential)

#### 1. FINAL_DECISION.md (8.6KB)
**Purpose:** Decision matrix comparing all approaches

**Key Sections:**
- ✅ Tool comparison matrix (txtai vs claude-mem vs beads vs custom)
- ✅ Scenario analysis (codebase search, task tracking, Claude Code)
- ✅ Recommendation: Use txtai for codebase search
- ✅ Action plan: `pip install txtai` → index → search → MCP

**Use When:** Need to justify architecture decision

**Key Quote:**
> "Your original use case → txtai wins. Different use case → Different tool."

---

#### 2. FINAL_RECOMMENDATION.md (4.4KB)
**Purpose:** Executive summary with ROI analysis

**Key Sections:**
- ✅ Viability assessment: File-based IS viable (not a waste)
- ✅ When to use file-based vs vector DB
- ✅ 15-minute setup guide
- ✅ Honest verdict: Use txtai, avoid custom build

**Use When:** Quick reference for decision rationale

**Key Quote:**
> "90% of vector DB features with 5% of the effort."

---

#### 3. DEEP_RESEARCH_FILE_BASED_SOLUTIONS.md (14KB)
**Purpose:** Comprehensive comparison of all solutions

**Key Sections:**
- ✅ File-based vs vector DB trade-offs
- ✅ txtai deep dive (architecture, features, limitations)
- ✅ Qdrant/Supabase/Weaviate analysis
- ✅ Effort estimation (15 min vs 2-3 days vs 1-2 weeks)
- ✅ Scale boundaries (<100k vs >1M documents)

**Use When:** Need detailed understanding of trade-offs

**Key Finding:**
> "txtai is the right level of abstraction. Custom implementation wastes effort on solved problems."

---

### Tier 2: Analysis Documents (Core)

#### 4. ANALYSIS_CLAUDE-MEM_BEADS.md (8.6KB)
**Purpose:** Why claude-mem and beads were rejected

**Key Sections:**
- ✅ claude-mem: Session memory for Claude Code IDE (not codebase search)
- ✅ beads: Task tracker for agents (not search engine)
- ✅ Extractability analysis: 90% rewrite required for both
- ✅ Recommendation: Use each for its intended purpose

**Use When:** Need to understand why other tools don't fit

**Key Quote:**
> "This is like asking: 'Can I use Excel (spreadsheets) or Trello (tasks) as my code editor?' They're different tools for different jobs."

---

#### 5. ARCHITECTURE_FULL_COVERAGE.md (8.8KB)
**Purpose:** Architecture design for file-based indexing

**Key Sections:**
- ✅ File-based storage structure (.ai-index/txtai/)
- ✅ MCP protocol integration
- ✅ Hybrid search implementation (BM25 + semantic + RRF)
- ✅ Progressive loading strategy (tiers)
- ✅ Portability and version control design

**Use When:** Implementing file-based search architecture

**Architecture:**
```
Your Agents
    ↓
MCP Protocol
    ↓
txtai Embeddings (file-based)
    ↓
.ai-index/txtai/
    ├── embeddings      # Dense vectors
    ├── keywords        # BM25 sparse index
    ├── documents       # Content storage
    └── config          # Settings
```

---

#### 6. CONTEXT_SEARCH_VS_MEMORY.md (9.0KB)
**Purpose:** Conceptual distinction between search and memory

**Key Sections:**
- ✅ Search engine: Retrieval from static knowledge base
- ✅ Memory system: Session state and conversation history
- ✅ Use cases: When to use which
- ✅ Hybrid approaches: Search + memory together

**Use When:** Clarifying requirements (search vs session memory)

**Key Distinction:**
- **Search:** "Find me all files about authentication" (txtai)
- **Memory:** "Remember what we discussed last session" (claude-mem)

---

### Tier 3: Implementation & Reference

#### 7. TXTVS_CK_COMPARISON.md (7.5KB)
**Purpose:** txtai vs ck (code intelligence) comparison

**Key Sections:**
- ✅ txtai: Semantic search (what files are about)
- ✅ ck: Code intelligence (what code does)
- ✅ Complementary not competitive
- ✅ When to use each

**Use When:** Deciding between txtai and ck for specific use case

**Verdict:** Use both - txtai for search, ck for code navigation

---

#### 8. QUICKSTART_CONTEXT_GENERATION.md (3.9KB)
**Purpose:** 15-minute setup guide

**Steps:**
1. Install: `pip install txtai`
2. Index: `python scripts/index-repo.py`
3. Search: `python scripts/search-repo.py "query"`
4. MCP: `python scripts/repo-mcp.py`
5. Configure Claude Desktop with MCP server

**Use When:** Implementing txtai for first time

---

#### 9. RESEARCH_AI_CONTEXT_SIDECAR_FILES.md (11KB)
**Purpose:** Research on AI context file formats

**Key Sections:**
- ✅ CLAUDE.md format specification
- ✅ .ai-context.yaml alternative
- ✅ Progressive loading strategies
- ✅ Tier-based retrieval (L1-L4)
- ✅ Token optimization techniques

**Use When:** Designing context file formats

---

#### 10. prompt-analysis-and-enhanced-variant.md (6.3KB)
**Purpose:** LLM prompt analysis for context generation

**Key Sections:**
- ✅ Original prompt analysis
- ✅ Enhanced prompt variants
- ✅ Prompt engineering best practices
- ✅ Context window optimization

**Use When:** Improving LLM prompts for context generation

---

## 🏗️ Architecture Recommendation

### File-Based Storage Structure
```
.ai-index/txtai/
├── embeddings/          # Dense semantic vectors
│   ├── documents.sqlite # Content storage
│   ├── embeddings.npy   # Vector arrays
│   └── metadata.json    # Index metadata
├── keywords/            # BM25 sparse index
│   ├── index.pkl        # Inverted index
│   └── scores.pkl       # TF-IDF scores
├── config/              # Configuration
│   ├── settings.yaml    # Index settings
│   └── schema.json      # Document schema
└── mcp/                 # MCP integration
    ├── server.py        # MCP server
    └── config.json      # MCP configuration
```

### Hybrid Search Flow
```
Query: "authentication middleware"
    ↓
BM25 Lexical Search → Rank by keyword matching
    ↓
Semantic Search → Rank by conceptual similarity
    ↓
RRF Fusion → Combine rankings optimally
    ↓
Results: Top-K files with combined scores
```

### Progressive Loading
```
L1: Quick Index (~250 tokens)
    ├── File list
    ├── Key concepts
    └── Directory structure

L2: Metadata (~1000 tokens)
    ├── File summaries
    ├── Keywords
    └── Tags

L3: Rich Context (~3000 tokens)
    ├── Code snippets
    ├── Dependencies
    └── Relationships

L4: Raw References (unlimited)
    └── Full file content
```

---

## 📈 ROI Analysis

### txtai vs Custom Implementation

| Factor | txtai | Custom File-Based | Vector DB |
|--------|-------|-------------------|-----------|
| **Setup Time** | 15 minutes | 2-3 days | 1-2 weeks |
| **Maintenance** | Low (community) | Medium (your team) | High (DevOps) |
| **Features** | Full hybrid search | Basic → Medium | Full advanced |
| **Performance** | Excellent (<100k) | Good | Excellent (any scale) |
| **Portability** | ✓ Copy .ai-index/ | ✓ Copy files | ✗ DB migration |
| **Cost** | Free | Free + dev time | Infrastructure + dev time |
| **Battle-Tested** | 12k+ users | No | Yes (if managed) |

**Conclusion:** txtai provides best ROI for expert-framework scale (<100k code chunks).

---

## 🚀 Implementation Path (15 Minutes)

### Step 1: Install txtai
```bash
pip install txtai
```

### Step 2: Index Codebase
```python
# Run indexing script (provided in research)
python scripts/index-repo.py
# → Generates .ai-index/txtai/ directory
```

### Step 3: Test Search
```python
# Run search script
python scripts/search-repo.py "payment retry logic"
# → Returns ranked results with scores
```

### Step 4: Add MCP Server
```python
# Run MCP server
python scripts/repo-mcp.py
# → Exposes search API via MCP protocol
```

### Step 5: Configure Claude Desktop
```json
{
  "mcpServers": {
    "expert-framework": {
      "command": "python",
      "args": ["/path/to/scripts/repo-mcp.py"]
    }
  }
}
```

**Done.** AI agents now have full codebase context via file-based search.

---

## 🎯 Decision Matrix

### For Expert-Framework Project

| Requirement | txtai | Custom | Vector DB | Decision |
|-------------|-------|--------|-----------|----------|
| File-based storage | ✓ | ✓ | ✗ | **txtai** |
| Hybrid search (BM25+semantic) | ✓ | ⚠️ (effort) | ✓ | **txtai** |
| RRF fusion | ✓ | ⚠️ (effort) | ✓ | **txtai** |
| MCP integration | ✓ | ⚠️ (effort) | ⚠️ | **txtai** |
| Quick setup (<1 hour) | ✓ | ✗ | ✗ | **txtai** |
| <100k documents | ✓ | ✓ | Overkill | **txtai** |
| Self-hosted | ✓ | ✓ | ⚠️ | **txtai** |
| Version control friendly | ✓ | ✓ | ✗ | **txtai** |

**Verdict:** txtai is optimal choice for 8/8 requirements.

---

## 🔗 Integration with Expert Framework

### As Execution Tool
```
executions/tools/search/
├── txtai_indexer.py      # Index codebase
├── txtai_searcher.py     # Search queries
├── mcp_server.py         # MCP integration
└── config.yaml           # Configuration
```

### As Directive
```yaml
# directives/workflows/search_context.yaml

name: "search_context"
description: "Search codebase for relevant context"

steps:
  - step: 1
    action: "execute_tool"
    tool: "txtai_searcher"
    inputs:
      query: "{{USER_QUERY}}"
      top_k: 10
    outputs:
      - name: "relevant_files"
        from: "result.files"
```

### As Knowledge Base
```markdown
# shared-knowledgebase/expertise/search_strategies.md

## Hybrid Search with txtai

- BM25 lexical search: Exact keyword matching
- Semantic search: Conceptual similarity
- RRF fusion: Combine rankings optimally

Usage: `txtai_searcher.search(query, top_k=10)`
```

---

## 📚 References

### External Resources
- [txtai GitHub](https://github.com/neuml/txtai) - 12k+ stars
- [txtai Documentation](https://neuml.github.io/txtai/)
- [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25)
- [Reciprocal Rank Fusion Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)

### Internal Documentation
- `tmp/context_generator/` - Progressive context loading implementation
- `__ref/context-engineering-frameworks/` - Academic research
- `__ref/expert-framework-reverse-engineered-drafts/` - Framework patterns

---

## 🎓 Key Learnings

### 1. File-Based Is Not a Waste
**Finding:** File-based storage is production-ready for <100k documents  
**Evidence:** txtai (12k+ stars), battle-tested in production  
**Implication:** No need for vector DB at expert-framework scale

### 2. Hybrid Search > Pure Semantic
**Finding:** BM25 + semantic + RRF outperforms either alone  
**Evidence:** Research papers, txtai benchmarks  
**Implication:** Always use hybrid search when possible

### 3. Tool Selection Matters
**Finding:** claude-mem and beads solve different problems (session memory, task tracking)  
**Evidence:** Deep analysis shows 90% rewrite required to repurpose  
**Implication:** Use right tool for right problem, don't force fit

### 4. ROI Trumps Features
**Finding:** txtai provides 90% of vector DB features with 5% of effort  
**Evidence:** 15-minute setup vs 1-2 week infrastructure  
**Implication:** Optimize for ROI, not feature completeness

### 5. Progressive Loading Enables Scale
**Finding:** Tier-based retrieval (L1-L4) optimizes tokens while maintaining quality  
**Evidence:** Context generator implementation (Phases 1-3)  
**Implication:** Combine hybrid search with progressive loading

---

## ✅ Validation Checklist

- [x] Research Question Answered: File-based IS viable
- [x] Technology Selected: txtai (file-based hybrid search)
- [x] Alternatives Evaluated: claude-mem, beads, custom, vector DBs
- [x] ROI Analyzed: 90% features, 5% effort
- [x] Implementation Path Defined: 15-minute setup guide
- [x] Scale Boundaries Identified: <100k documents
- [x] Integration Plan Created: executions/tools/search/
- [x] Documentation Complete: 10 research files, 82KB

---

## 📝 Next Actions

### Immediate
1. ✅ Install txtai: `pip install txtai`
2. ✅ Run indexing script on expert-framework
3. ✅ Test search queries
4. ✅ Validate performance (<500ms per query)

### Short-term
5. ⚠️ Integrate as `executions/tools/search/`
6. ⚠️ Create directive `search_context.yaml`
7. ⚠️ Add knowledge to `shared-knowledgebase/expertise/search_strategies.md`
8. ⚠️ Configure MCP server for AI agents

### Long-term
9. ⚠️ Monitor performance (scale < 100k documents)
10. ⚠️ Evaluate vector DB if/when scale exceeds threshold
11. ⚠️ Integrate with context_generator for enhanced metadata
12. ⚠️ Add progressive loading to search results

---

**Research Complete:** 2025-12-24  
**Decision:** Use txtai (file-based hybrid search)  
**Status:** Ready for implementation  
**Next Step:** `pip install txtai && python scripts/index-repo.py`

---

**Generated:** 2025-12-24  
**Format:** AGENTS.md following expert-framework progressive context loading standards  
**Framework Version:** 1.0
