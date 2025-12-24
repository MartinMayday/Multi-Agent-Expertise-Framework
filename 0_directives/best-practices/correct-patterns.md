# ✅ Correct Patterns

## 1. Sequential Chaining with TaskOutput
Always retrieve and verify the output of a previous step before proceeding.
```yaml
- step: 1
  action: "execute_tool"
  gate: "await_completion"
```

## 2. KB-First Research
Always check the shared knowledge base before initiating external research.

## 3. Evidence-Based Answering
Always cite specific files and line numbers when answering questions about the codebase.

## 4. Minimal Edits
Keep code modifications focused and preserve existing formatting.
