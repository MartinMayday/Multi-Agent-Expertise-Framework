---
title: "Agent Expert Framework Handoff (GEMINI.md)"
filename: "GEMINI.md"
complexity: "advanced"
audience: "backend-engineers"
category: "Instruction Stack"
keywords:
  - "expert-framework"
  - "agentic-workflow"
  - "context-engineering"
  - "first-principles"
  - "sdd"
  - "clear"
  - "prp"
  - "prd"
  - "expertise-yaml"
  - "orchestration"
tags:
  - "agent-framework"
  - "prompt-engineering"
  - "automation"
summary: |
  A consolidated context-engineering file designed for a planning AI/LLM to execute the "expert-framework". It integrates CLEAR, SDD, and First Principles frameworks into a cohesive agentic workflow system. Includes preflight checklists and retrieval-ready summaries of core principles.
rrf_anchors:
  - "handoff-file"
  - "agent-expert-spec"
  - "scaffolding-prompt"
context_snippet: |
  [MANDATORY HEURISTICS]
  This file serves as the primary handoff document for initializing the "expert-framework". It replaces assumptions with structured placeholders and enforces Spec-Driven Development (SDD). Agents must follow the CLEAR framework for all prompt generation and use First Principles for architectural deconstruction.

  [NEGATIVE CONSTRAINTS]
  DO NOT assume codebase structure without verifying against local files or provided snippets. DO NOT ignore frontmatter requirements for new files.
---

# 🚀 Agent Expert Framework: Handoff & Execution

This document provides the foundational context and executable instructions for building a production-ready, file-based agentic workflow system.

## 📋 Preflight Checklist
- [ ] **Context Verification**: Confirm all `__ref/` files have been internalized.
- [ ] **Identity Alignment**: Ensure you are operating as an "Expert Framework" Orchestrator.
- [ ] **Tooling Check**: Verify access to filesystem (read/write), web-search/scrape, and subagent spawning tools.
- [ ] **First Principles Sweep**: Identify and challenge all "legacy thinking" or analogies in the current project scope.
- [ ] **Placeholder Mapping**: Replace all `[[PLACEHOLDER]]` values with project-specific data before execution.

---

## 🧠 Distilled Context: The Expert Framework

### 1. Core Principles
- **Self-Improving Mental Models**: The system uses `expertise.yaml` files as long-term memory. Agents validate and update these files post-execution to "learn".
- **Specialized Experts**: Small, focused agents (e.g., `database-expert`, `frontend-expert`) with narrow scopes and specific toolsets.
- **Workflow Chaining**: Complex tasks are broken into `Plan -> Build -> Improve` cycles using subagents.
- **Spec-Driven Development (SDD)**: Specifications are the source of truth. Implementation is a derivative behavior.

### 2. File-Based Architecture
- **`.claude/experts/`**: Root directory for expert configurations and expertise files.
- **`expertise.yaml`**: Contains project-specific Information, Examples, Patterns, and Rules.
- **Commands/Skills**: Markdown files with frontmatter defining the tool permissions and workflow for a specific task.

---

## 🛠️ Reference File Retrieval Snippets

### [Framework: CLEAR Prompting]
**File**: `clog_braindump-and-defining-missing-files.md`
**Summary**: A guide for high-performance prompt engineering using Context, Lens, Expectations, Accuracy, and Result.
**Context Snippet**: Mandatory for all agent-to-agent prompt generation. Ensures clarity and minimizes hallucinations by specifying output structure and success criteria.

### [Agile: Epic Breakdown]
**File**: `epic-breakdown.md`
**Summary**: Framework for structuring initiatives into Epic > Feature > User Story > Task hierarchies.
**Context Snippet**: Use to map the implementation roadmap. Ensures every step has clear stakeholder value and measurable acceptance criteria.

### [Process: Spec-Driven Development (SDD)]
**File**: `spec-generation.md`
**Summary**: Protocols for ensuring implementation is derived from version-controlled technical specifications.
**Context Snippet**: The project's "Source of Truth" rule. Requirement Change -> Update Spec -> Regenerate Implementation.

### [Execution: PRP Flow]
**File**: `create-prp.md`
**Summary**: A workflow for creating Product Requirement Prompts (PRP) via thorough documentation review, web research, template analysis, and codebase exploration.
**Context Snippet**: Essential for the "Build" phase to ensure agents have all necessary library and implementation patterns.

### [Planning: PRD Standards]
**File**: `create-prd.md`
**Summary**: Templates for defining product requirements, focusing on user needs and business value over technical implementation.
**Context Snippet**: The entry point for all new features. Defines "what" and "why".

### [Reasoning: First Principles]
**File**: `first-principles-thinking.md`
**Summary**: A system for breaking complex problems into reductionist truths to build novel, constraint-free solutions.
**Context Snippet**: Use during the "Planning" phase or after 3+ execution failures to reframe the problem.

### [Metadata: Frontmatter Protocol]
**File**: `frontmatter-template.md`
**Summary**: YAML schema optimized for hybrid search (Vector + BM25) and reciprocal rank fusion.
**Context Snippet**: All new framework files MUST include this frontmatter to maintain system discoverability.

---

## 📝 Proposed Context Enrichment (Missing Sources)
The following sources are highly recommended to be scraped/crawled to finalize the "expert-framework" setup:
1. **`concept_library/cc_PRP_flow/README.md`**: To understand the full PRP architecture referenced in `create-prp.md`.
2. **IndyDevDan's "Agent Expert" Repository**: For the latest version of the `expertise.yaml` schema and `Task()` tool signature.
3. **`ai_docs/` local directory**: If it exists, it should be the first place the agent looks for technical baseline rules.

---

## 🧬 Framework Scaffolding (Placeholders)
The next agent should replace these placeholders to build the initial system:

- **Project Root**: `[[PROJECT_ROOT_PATH]]` (e.g., `/Volumes/uss/cloudworkspace/...`)
- **Primary Domain**: `[[PRIMARY_DOMAIN]]` (e.g., "AI Developer Tools")
- **Expert 1 (Lead)**: `[[EXPERT_NAME_PLANNER]]` -> Target: `.claude/experts/planner/`
- **Expert 2 (Domain)**: `[[EXPERT_NAME_DOMAIN]]` -> Target: `.claude/experts/[[DOMAIN_KEY]]/`
- **Initial Feature**: `[[INITIAL_FEATURE_BREAKDOWN]]` (Reference a PRD/Epic snippet)

---

> [!IMPORTANT]
> This file is a **Handoff Objective**. Upon loading this file, the NEXT AGENT must initialize the workspace, create the `.claude/experts` structure, and begin with **Step 1: First Principles Analysis** of the current user request.
