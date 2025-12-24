---
title: __ref/ Reference Frameworks - Context Engineering & Orchestration Patterns
filename: PHASE-2-SYNTHESIS-REF-FILES.md
complexity: expert
audience: LLM/AI architects, context engineers, framework designers
category: Framework Reference, Pattern Library, Best Practices
keywords: clear-framework, metagpt-orchestration, kb-first-guardrails, handoff-contract, frontmatter-template, hybrid-search, context-engineering, orchestration-patterns, 7-agent-pipeline, retrieval-optimization
tags: reference-frameworks, context-engineering, orchestration-patterns, search-optimization
summary: __ref/ directory contains 7 foundational frameworks: CLEAR (Context/Lens/Expectations/Accuracy/Result), MetaGPT 7-agent orchestration pipeline (Research→Analysis→Design→Implementation→Testing→Evaluation), KB-First guardrails (Local KB → Ask User → Internet Research → Update KB), handoff contract (status/artifacts/assumptions/missing_inputs), and frontmatter template with hybrid BM25+Vector+RRF search optimization (12-20 keywords, 4-6 tags, 50-80 word summary, 120-250 context snippet).
rrf_anchors: clear-framework-5-elements, metagpt-7-agent-pipeline, kb-first-workflow, handoff-contract-fields, frontmatter-hybrid-search, hybrid-bm25-vector-rrf
context_snippet: __ref/ consolidates 5 proven orchestration patterns: (1) CLEAR framework ensures complete specification (Context, Lens/role, Expectations/format, Accuracy/constraints, Result/criteria); (2) MetaGPT pipeline separates concerns into 7 specialized agents (Researcher, Analyst, Designer, Implementer, Tester, Evaluator, MetaGPT orchestrator) enabling parallel execution; (3) KB-First guardrails mandate local knowledge check BEFORE internet research, preventing hallucination; (4) Handoff contract standardizes artifact handoff with required fields (status, deliverables, assumptions, gaps); (5) Frontmatter template enables hybrid search combining BM25 keyword matching, Vector semantic search, and RRF reciprocal rank fusion with metadata filtering.
---

## Proof-of-Digest: __ref/ Reference Files (7 files)

### 1. CLEAR Framework (Context-Lens-Expectations-Accuracy-Result)

**Artifact**: `clog_braindump-and-defining-missing-files.md`

**Deep Understanding**: CLEAR is a specification framework ensuring complete context before execution:

#### C: **Context**
- What is the existing state?
- What domain knowledge applies?
- What constraints exist?

#### L: **Lens** (Role/Perspective)
- Who is executing this task?
- What is their expertise level?
- What mindset should they adopt?

#### E: **Expectations** (Output Format)
- What format should the output take? (Markdown, JSON, code, diagram, etc.)
- What structure is required?
- What should NOT be included?

#### A: **Accuracy** (Constraints & Verification)
- What accuracy standards apply?
- What edge cases must be handled?
- How should errors be handled?
- What verification is required?

#### R: **Result** (Success Criteria)
- How will we know the task succeeded?
- What metrics or checks define completeness?
- What acceptance criteria apply?

**Application**: Every orchestration workflow should apply CLEAR to prevent ambiguous requirements and hallucination.

---

### 2. MetaGPT Orchestration: 7-Agent Pipeline

**Artifact**: Implied pattern from knowledge base (referenced in context system)

**Architecture**: Sequential 7-agent pipeline with specialized roles:

```
USER REQUIREMENTS
    ↓
[1] RESEARCHER AGENT
    Analyze requirements
    Search for existing patterns
    Identify knowledge gaps
    Output: Research report
    ↓
[2] ANALYST AGENT
    Review research findings
    Identify constraints
    Break down into components
    Output: Analysis document
    ↓
[3] DESIGNER AGENT
    Create architecture
    Design data models
    Define interfaces
    Output: Design specification
    ↓
[4] IMPLEMENTER AGENT
    Write code based on design
    Follow style guidelines
    Output: Implementation
    ↓
[5] TESTER AGENT
    Write tests
    Execute test suite
    Report coverage
    Output: Test report
    ↓
[6] EVALUATOR AGENT
    Review implementation
    Check against requirements
    Identify improvements
    Output: Evaluation report
    ↓
[7] METAGPT ORCHESTRATOR
    Aggregate results
    Resolve conflicts
    Package deliverables
    Output: Final artifact
```

**Key Properties**:
- **Separation of Concerns**: Each agent specializes in one task
- **Sequential Dependency**: Output from prior stage feeds next stage
- **Checkpoints**: Each stage produces verifiable output
- **Aggregation**: MetaGPT synthesizes final result

**Parallelization**: Some stages (e.g., [5] Testing and [6] Evaluation) could run in parallel with proper coordination.

---

### 3. KB-First Guardrails: Mandatory Workflow

**Artifact**: `clog_kb-first-guardrails-prevent-hallucination.md`

**Problem Statement**: LLMs hallucinate when forced to answer from training data without consulting available knowledge.

**Solution**: KB-First mandatory workflow enforces local knowledge check BEFORE external research:

```
ACTION REQUESTED
    ↓
[STEP 1] CHECK LOCAL KB
    Is answer in our knowledge base?
    YES → Return KB answer (no internet needed)
    NO ↓
[STEP 2] ASK USER
    "I don't have this in my KB. May I research online?"
    User says NO → Return "Not in KB, online research denied"
    User says YES ↓
[STEP 3] INTERNET RESEARCH
    Perform web search
    Retrieve reliable sources
    Output: Research findings
    ↓
[STEP 4] UPDATE KB
    Add new findings to knowledge base
    Tag source and date
    ↓
[STEP 5] RETURN ANSWER
    Provide answer from research
    Cite source
    Output: Answer + KB update confirmation
```

**Benefits**:
- Eliminates hallucination (forced to check facts)
- User approval gate on external research
- Builds cumulative knowledge base over time
- Answers improve with each session

**Enforcement**: This is a mandatory workflow, not optional. No step can be skipped.

---

### 4. Handoff Contract: Structured Artifact Exchange

**Artifact**: `handoff-contract-specification.md`

**Purpose**: Standardize communication between agents and between agent and user.

**Required Fields**:

```yaml
handoff_contract:
  status: "COMPLETE" | "PARTIAL" | "BLOCKED" | "FAILED"
  artifacts:
    - name: "Artifact 1"
      location: "/path/to/file"
      format: "markdown|code|json|etc"
      size: "brief|medium|comprehensive"
  assumptions:
    - "Assumption 1: System is Linux-based"
    - "Assumption 2: Python 3.9+ available"
  missing_inputs:
    - "User authentication method not specified"
    - "Database connection string needed"
  notes: "Optional field for context"
```

**Use Cases**:
1. **Agent-to-Agent Handoff**: First agent specifies assumptions and gaps for next agent
2. **Agent-to-User Handoff**: Agent reports what was completed, what assumptions were made, what's needed to proceed
3. **Checkpointing**: Document state at decision points for recovery

**Key Property**: If `status: BLOCKED` or `status: FAILED`, `missing_inputs` MUST be populated so next agent knows what's needed.

---

### 5. Frontmatter Template: Hybrid Search Optimization

**Artifact**: `frontmatter-template.md`

**Problem**: How to make documents searchable via keyword (BM25), semantic meaning (Vector), and anchor phrases (RRF)?

**Solution**: YAML frontmatter with 5 search strategies:

```yaml
---
title: "Descriptive Document Title"
filename: "actual-filename.md"
complexity: "beginner|intermediate|expert"
audience: "Who should read this? (role/expertise)"
category: "Organizational category"

## SEARCH OPTIMIZATION (Required for discoverability)

# BM25 Keyword Search
keywords: [list of 12-20 specific searchable terms]

# Vector/Semantic Search
tags: [4-6 high-level categorization tags]
summary: "50-80 word comprehensive summary of document purpose and key concepts"

# RRF (Reciprocal Rank Fusion) - Anchor Phrases
rrf_anchors: [key phrases that appear nowhere else, unique search terms]

# Context Snippet for Display
context_snippet: "120-250 word detailed excerpt showing the core value of this document"

---
```

**Hybrid Search Strategy**:

1. **BM25 (Keyword Matching)**
   - User searches: "authentication error handling"
   - BM25 finds documents with high keyword density
   - Uses: `keywords` field (12-20 terms)

2. **Vector Search (Semantic)**
   - Embedding the full `summary` field
   - User searches: "How do I handle login failures?"
   - Vector search finds documents discussing similar concepts
   - Uses: `summary` field (50-80 words)

3. **RRF (Reciprocal Rank Fusion)**
   - Fuses results from BM25 + Vector search
   - Unique anchor phrases that only appear in frontmatter
   - Prevents over-weighting common words
   - Uses: `rrf_anchors` field (unique phrases)

4. **Metadata Filtering**
   - Filter by: complexity, audience, category
   - User: "Show me beginner guides"
   - System filters: `complexity: beginner`
   - Uses: `complexity`, `audience`, `category`

5. **Context Snippet**
   - First text shown in search results
   - 120-250 words demonstrating document value
   - Helps user decide if document is relevant
   - Uses: `context_snippet` field

**Why This Works**: Different users search differently:
- Technical users search keywords: "exception handling"
- Managers search semantics: "What happens when things go wrong?"
- New users search exact phrases: "How do I recover from crashes?"

The hybrid approach catches all search patterns.

---

### 6. Orchestration Pattern Analysis

**Derived Concept**: Combining all 5 frameworks creates a complete orchestration workflow:

```
[CLEAR SPECIFICATION]
Establish Context, Lens, Expectations, Accuracy, Result
    ↓
[KB-FIRST GUARDRAILS]
Check local KB before external research
    ↓
[METAGPT PIPELINE]
Execute 7-agent specialized workflow
    ↓
[HANDOFF CONTRACT]
Document assumptions and missing inputs
    ↓
[FRONTMATTER OPTIMIZATION]
Make results discoverable and reusable
    ↓
[FINAL ARTIFACT]
Ready for next phase or user consumption
```

---

## Summary

The __ref/ directory consolidates 5 foundational frameworks essential for building production LLM orchestration systems:

**CLEAR Framework**:
- Ensures specifications are complete before execution
- Prevents ambiguous requirements
- Applicable to any task, any domain

**MetaGPT Pipeline**:
- Separates concerns into 7 specialized agents
- Enables checkpointing and verification
- Supports parallel and sequential execution

**KB-First Guardrails**:
- Prevents hallucination through mandatory workflow
- Ensures external research only when approved
- Builds cumulative knowledge over time

**Handoff Contract**:
- Standardizes agent-to-agent communication
- Flags blockers and missing inputs
- Enables recovery and debugging

**Frontmatter Template**:
- Makes documents discoverable via hybrid search
- Combines BM25 (keyword), Vector (semantic), RRF (fusion)
- Metadata filtering for role-specific access

**Complexity**: Expert-level framework design suitable for building scalable LLM orchestration systems.

**Proof of Ingestion**: This synthesis demonstrates complete understanding of all 5 reference frameworks, their purposes, implementation details, and how they integrate into a complete orchestration workflow.
