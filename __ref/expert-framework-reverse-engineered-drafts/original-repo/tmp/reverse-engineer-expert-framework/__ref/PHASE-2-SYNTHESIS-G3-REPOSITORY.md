---
title: G3 Repository - Planning Mode & Provider Architecture Synthesis
filename: PHASE-2-SYNTHESIS-G3-REPOSITORY.md
complexity: expert
audience: LLM/AI agents, platform architects
category: Framework Components, Architecture Reference
keywords: planning-mode, state-machine, providers, anthropic, openai, embedded, error-handling, retry-logic, flock-mode, multi-agent, autonomous-execution, thinking-mode, cache-control, token-tracking, context-thinning, todo-persistence, code-search, tree-sitter
tags: g3-framework, planning-orchestration, llm-providers, error-recovery, multi-agent-ensemble
summary: G3 repository (36756 lines) implements a complete planning-mode orchestration framework with multi-provider LLM support (Anthropic Claude, OpenAI, Databricks OAuth, embedded llama.cpp), autonomous retry logic with exponential backoff, state-machine driven planning workflow, and flock-mode for parallel multi-agent segment execution with token tracking and context thinning strategies.
rrf_anchors: planning-state-machine, provider-architecture, autonomous-retry-config, flock-mode-partitioning, cache-control-implementation, thinking-mode-logic, context-management-tokens, error-classification-recoverable
context_snippet: G3 core architecture separates concerns into: (1) Planning state machine managing STARTUP→REFINE→IMPLEMENT→COMPLETE lifecycle with recovery paths; (2) Multi-provider abstraction supporting Anthropic (thinking mode, cache control, 1M context), OpenAI (streaming, tool calling), Databricks (OAuth+refresh), Embedded (llama.cpp auto-download); (3) Autonomous retry with 6 attempts over 10min using [10s,30s,60s,120s,180s,200s] base delays + ±30% jitter; (4) Flock mode partitions requirements into logical modules, clones repos, runs segments in parallel with status tracking; (5) Context management via token tracking at 50%-80% thresholds with auto-summarization, tool result thinning (>500 chars), but NEVER thins TODO results.
---

## Proof-of-Digest: G3 Repository (36756 lines)

### Planning Mode State Machine Architecture

**Artifact Location**: `crates/g3-planner/src/planner.rs` (lines 28668-28683 for critical commit invariant)

**Deep Understanding**: The planning mode implements a robust state machine controlling execution flow:

```
STARTUP → PROMPT FOR NEW REQUIREMENTS → REFINE REQUIREMENTS → IMPLEMENT REQUIREMENTS → IMPLEMENTATION COMPLETE
   ↑                                                                   ↑         ↑                           ↓
   +--- RECOVERY (Resume) ─────────────────────────────────────────────+         |                           |
   +--- RECOVERY (Mark Complete) ───────────────────────────────────────────────+                           |
   +──────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

**Key Directory Structure** (`<codepath>/g3-plan/`):
- `planner_history.txt` - Audit log with timestamp entries (REFINING, GIT HEAD, START IMPLEMENTING, COMPLETED, GIT COMMIT)
- `new_requirements.md` - User-supplied requirements, moved to current_requirements when approved
- `current_requirements.md` - Active implementation requirements
- `todo.g3.md` - Task tracking with SHA256 staleness detection (`Based on the requirements file with SHA256: <SHA>`)
- `completed_requirements_<timestamp>.md` - Historical requirements archive
- `completed_todo_<timestamp>.md` - Historical TODO archive

**CRITICAL INVARIANT**: Write GIT COMMIT entry to planner_history BEFORE executing git commit. This ordering regressed multiple times during refactoring. The invariant is:
```rust
history::write_git_commit(&config.plan_dir(), summary)?;  // WRITE FIRST
git::stage_plan_dir(&config.codepath, &config.plan_dir())?;  // RE-STAGE
let _commit_sha = git::commit(&config.codepath, summary, description)?;  // EXECUTE
```

**Proof**: Real planner_history.txt (lines 36459-36580) shows multiple refinement cycles with recovery attempts and timestamps documenting the actual workflow.

---

### Multi-Provider LLM Architecture

**Artifact Location**: `crates/g3-providers/src/` (lines 30443-33940)

**Deep Understanding**: The provider system abstracts 4 provider types:

#### 1. **Anthropic Provider** (30443-31662)
- **Features**:
  - Native tool calling with function definitions
  - **Cache Control**: Three modes with TTL: `ephemeral()`, `five_minute()` (TTL: "5m"), `one_hour()` (TTL: "1h")
  - **Extended Thinking Mode**: Budget tokens configuration, requires `max_tokens > thinking_budget_tokens + 1024`
  - **1M Context Window**: Via header `anthropic-beta: context-1m-2025-08-07`
  - **Streaming SSE**: Handles `message_start`, `content_block_start`, `content_block_delta`, `content_block_stop`, `message_stop` events
  - **Tool Call Parsing**: Supports args in `content_block_start` (complete) or `content_block_delta` (incremental JSON)

**Cache Control Logic** (crates/g3-providers/tests/cache_control_*.rs, lines 33943-34321):
```json
// CORRECT serialization format - type + ttl fields
{"type": "ephemeral", "ttl": "5m"}

// NEVER serialize to nested structure
{"cache_control": {"type": "ephemeral"}}  // ❌ WRONG
```

#### 2. **Embedded Provider** (31667-32496)
- **Model Auto-Download**: Qwen 2.5 7B Q3_K_M (~3.5GB) from HuggingFace if missing
- **Message Formatting**:
  - Qwen: `<|im_start|>role\ncontent<|im_end|>`
  - Mistral: `<s>[INST] ... [/INST] response</s>`
  - Llama: `[INST] <<SYS>>...<</SYS>> ... [/INST]`
- **Stop Sequences**: Model-specific (Qwen: `<|im_end|>`, Llama: `</s>`/`[/INST]`)
- **Streaming**: Buffers partial sequences to avoid premature truncation at boundaries

#### 3. **OpenAI Provider** (33398-33940)
- **Features**: Native tool calling, streaming, usage tracking in stream
- **Config**: Uses `max_completion_tokens` (not `max_tokens`), `stream_options.include_usage: true`
- **Streaming Tool Calls**: Accumulates delta tool calls by index, parses function arguments incrementally

#### 4. **Databricks Provider with OAuth** (32929-33394)
- **Token Storage**: Cached in `~/.config/g3/databricks/oauth/<hash>.json`
- **Token Refresh**: Automatic refresh using `refresh_token`, falls back to new OAuth flow if refresh fails
- **PKCE Flow**: S256 code challenge, state parameter for CSRF protection
- **Local OAuth Server**: Axum server on localhost for callback (127.0.0.1:port)

**Provider Registry** (crates/g3-providers/src/lib.rs, lines 32500-32925):
- Message ID format: `HHMMSS-XXX` (3 random alpha chars), NOT serialized to JSON
- HashMap-based registry with default provider fallback
- Config structure (`[providers]` section):
  - `default_provider = "anthropic.default"` (format: `<provider_type>.<config_name>`)
  - Optional role-specific overrides: `planner`, `coach`, `player`
  - Fallback if role-specific not specified

---

### Autonomous Retry & Error Handling System

**Artifact Location**: `crates/g3-core/src/error_handling.rs` (lines 16219-16266)

**Error Classification**:
- **Recoverable**: RateLimit (429), NetworkError, ServerError (5xx), ModelBusy, Timeout, TokenLimit, ContextLengthExceeded
- **Non-Recoverable**: All other errors → immediate failure

**Retry Configuration**:
- **Default Mode**: 3 attempts
- **Autonomous Mode**: 6 attempts
- **Base Delays**: [10s, 30s, 60s, 120s, 180s, 200s] = 600s total (10 minutes)
- **Jitter**: ±30% random distribution to prevent thundering herd

```rust
fn calculate_autonomous_retry_delay(attempt: u32) -> Duration {
    let base_delays_ms = [10000, 30000, 60000, 120000, 180000, 200000];
    let base_delay = base_delays_ms.get(attempt.saturating_sub(1) as usize).unwrap_or(&200000);
    let jitter = (*base_delay as f64 * 0.3 * rng.gen::<f64>()) as u64;
    Duration::from_millis(if rng.gen_bool(0.5) { base_delay + jitter } else { base_delay.saturating_sub(jitter) })
}
```

**Forensic Logging**: Error context saved to `logs/errors/error_{timestamp}_{session_id}.json` capturing operation, provider, model, prompt, request/response, stack trace, token count.

---

### Flock Mode: Multi-Agent Parallel Execution

**Artifact Location**: `crates/g3-ensembles/src/flock.rs` (lines 23476-23523)

**Architecture**:
1. **Partitioning Phase**: LLM analyzes requirements → partition JSON with module names, requirements text, dependencies
2. **Cloning Phase**: Clone git repo N times for each segment (isolated workspaces)
3. **Parallel Execution**: Run segments concurrently using Tokio async executor
4. **Aggregation Phase**: Merge results with metrics tracking

**Partitioning JSON Format**:
```json
[
  {
    "module_name": "string",
    "requirements": "string (text for this module)",
    "dependencies": ["array", "of", "other", "module", "names"]
  }
]
```

**Status Tracking** (`flock-status.json`):
- SegmentStatus: segment_id, workspace, state, timestamps, metrics (tokens, tool_calls, errors)
- SegmentState: Pending, Running, Completed, Failed, Cancelled (with emoji display)

---

### Context Management & Token Tracking

**Artifact Location**: `crates/g3-core/src/context.rs` (implied from summary)

**Token Tracking**:
- `used_tokens`: Tracked via `add_message()` for cumulative count
- `cumulative_tokens`: Updated via `update_usage_from_response()`
- Thresholds: 50%, 60%, 70%, 80% with `last_thinning_percentage` tracking

**Thinning Strategy**:
- **Auto-Summarization**: Triggered at 80% capacity
- **Context Preservation**: System prompt + README/AGENTS.md always preserved in first two messages
- **Tool Result Thinning**: Replaces large results (>500 chars) with file references in first third of conversation
- **TODO Exemption**: `todo_read` and `todo_write` results NEVER thinned (preserves task continuity)

---

### TODO System: File-Based Persistence

**Artifact Location**: `todo.g3.md` in workspace root

**Features**:
- **SHA256 Staleness Detection**: First line `Based on the requirements file with SHA256: <SHA>`
- **Completion Detection**: All `- [ ]` converted to `- [x]` or `- [X]`
- **Auto-Deletion**: Removes file when all tasks complete (configurable)
- **Session Survival**: Persists across context boundaries and session restarts

---

### Code Search with Tree-Sitter

**Artifact Location**: `crates/g3-core/src/code_search/searcher.rs` (lines 20157-20173)

**Supported Languages**: Rust, Python, JavaScript, TypeScript, Go, Java, C, C++, Haskell, Scheme

**Query Implementation**:
```rust
fn is_language_file(path: &Path, language: &str) -> bool {
    match (language, ext) {
        ("rust", Some("rs")) => true,
        ("python", Some("py")) => true,
        ("javascript" | "js", Some("js" | "jsx" | "mjs")) => true,
        ("typescript" | "ts", Some("ts" | "tsx")) => true,
        // ... etc
    }
}
```

---

### Integration Tests & Validation

**Artifact Location**: `crates/g3-planner/tests/` (lines 30015-30401)

**Test Coverage**:
- **logging_test.rs**: Validates log file creation in `logs/` with format `YYYYMMDD_HHMMSS`
- **planner_test.rs**: Tool message format, codebase exploration, shell command extraction
- **retry_feedback_test.rs**: RetryConfig presets, approval detection via "IMPLEMENTATION_APPROVED" keyword

**Key Lessons Learned**:
1. **Ordering Invariants Fragile**: History write-before-commit regressed multiple times
2. **UI Testing Essential**: Tool output whitespace persisted 5 iterations without app testing
3. **Environment Variables Cross Async Boundaries**: G3_WORKSPACE_PATH must be set BEFORE async initialization
4. **Testing Methodology Matters**: "Run actual app" became explicit requirement after multiple failures

---

## Summary

The G3 repository is a production-grade orchestration framework for AI/LLM planning with:
- Robust state machine controlling the full planning lifecycle with recovery paths
- Multi-provider abstraction supporting 4 distinct provider types with provider-specific optimizations
- Autonomous retry logic with sophisticated delay distribution and forensic logging
- Flock mode enabling parallel multi-agent execution with logical module partitioning
- Token-aware context management with thinning strategies that preserve critical data
- File-based TODO persistence surviving across session boundaries
- Tree-sitter based code search supporting 10+ languages
- Real-world planning history audit logs proving the system works in practice

**Complexity**: Expert-level architecture requiring deep understanding of async Rust, LLM APIs, state machines, and distributed execution patterns.
