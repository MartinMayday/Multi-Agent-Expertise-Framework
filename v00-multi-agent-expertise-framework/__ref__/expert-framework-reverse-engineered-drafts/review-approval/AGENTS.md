# Agent Catalog

This catalog lists all available agents in the system. Agents can reference this to discover capabilities and request delegation.

## MetaGPT (Orchestrator)
- **Role**: Prompt decomposition and workflow coordination
- **Invocation**: Automatic on braindump prompts
- **Model**: claude-sonnet-4.5
- **Tools**: None (orchestration only)
- **Location**: agents/metagpt/

## ResearchGPT
- **Role**: Documentation-first research
- **Triggers**: "research", "find documentation", "gather info"
- **Model**: claude-sonnet-4.5
- **Tools**: web.search, web.scrape, web.fetch
- **Location**: agents/researchgpt/

## AnalysisGPT
- **Role**: Pattern extraction and synthesis
- **Triggers**: "analyze", "synthesize", "compare"
- **Model**: claude-sonnet-4.5
- **Tools**: None (analysis only)
- **Location**: agents/analysisgpt/

## DesignGPT
- **Role**: System design and architecture
- **Triggers**: "design", "architect", "plan system"
- **Model**: claude-sonnet-4.5
- **Tools**: None (design only)
- **Location**: agents/designgpt/

## ImplementationGPT
- **Role**: Code generation from specifications
- **Triggers**: "implement", "build", "code"
- **Model**: claude-sonnet-4.5
- **Tools**: Write, Read, Bash
- **Location**: agents/implementationgpt/

## TestGPT
- **Role**: Validation and testing
- **Triggers**: "test", "validate", "verify"
- **Model**: claude-sonnet-4.5
- **Tools**: Bash, Read
- **Location**: agents/testgpt/

## EvaluationGPT
- **Role**: Go/no-go decisions and handoff coordination
- **Triggers**: "evaluate", "decide", "handoff"
- **Model**: claude-sonnet-4.5
- **Tools**: Read, Write (reports only)
- **Location**: agents/evaluationgpt/

## Request New Agent
If no existing agent fits your needs, return to MetaGPT with:
- Required capabilities
- Expected inputs/outputs
- Suggested name

---

## Repo Context System

This repository uses a **repo-context memory system** (`.context/`) that enables agents and humans to build upon earlier work, never starting from scratch.

### Core Context Files

- **`.context/core/rules.md`** - Hard rules (ALWAYS check first before any action)
- **`.context/core/identity.md`** - Repo identity, mission, purpose
- **`.context/core/preferences.md`** - Repo-level preferences for agents/humans
- **`.context/core/workflows.md`** - Repo SOPs (staging, validation, promotion)
- **`.context/core/session.md`** - Current session focus
- **`.context/core/journal.md`** - Append-only notable decisions

### Conversation Transcripts

Full conversation transcripts are stored in `.context/conversations/` with:
- Session ID, timestamp, participants
- Tools used
- Redaction markers for secrets

See `.context/README.md` for full documentation.

---

## IDE Entrypoints

This framework is **IDE/CLI agnostic**. Entrypoint files provide consistent behavior across different AI coding environments:

- **`.cursorrules`** - Cursor IDE entrypoint
- **`CLAUDE.md`** - Claude Code entrypoint
- **`GEMINI.md`** - Gemini tooling entrypoint

All entrypoints enforce the same core principles:
- KB-first execution
- Staging-only writes
- Context memory system
- No assumptions, no secrets

See individual entrypoint files for IDE-specific instructions.
