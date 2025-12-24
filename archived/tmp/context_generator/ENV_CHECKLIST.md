# Environment Variable Checklist

## Required Variables

Only **one** of these is used, depending on which provider you configure:

```bash
# Pick ONE model for the tool to use
CONTEXT_GENERATOR_MODEL=offline                                 # Static analysis only (no LLM)
CONTEXT_GENERATOR_MODEL=ollama/llama3.2                        # Local Ollama
CONTEXT_GENERATOR_MODEL=openrouter/anthropic/claude-3-haiku    # OpenRouter cloud
CONTEXT_GENERATOR_MODEL=gemini/gemini-1.5-flash                # Google Gemini
CONTEXT_GENERATOR_MODEL=moonshot/moonshot-v1-8k                # Moonshot AI
CONTEXT_GENERATOR_MODEL=zai/gpt-4-turbo                        # ZAI enterprise
```

**Important**: 
- Format is `provider/model` (e.g., `openrouter/anthropic/claude-3-haiku`)
- Not `<PROVIDER>_MODEL=` (that's wrong)
- Only set ONE model string in CONTEXT_GENERATOR_MODEL

## Provider-Specific Variables (Required per provider)

### For OpenRouter:
```bash
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

### For Ollama:
```bash
OLLAMA_HOST=http://localhost:11434    # Default, rarely needs changing
```

### For LM Studio:
```bash
LMSTUDIO_HOST=http://localhost:1234
LMSTUDIO_API_KEY=lm-studio    # Default, rarely needs changing
```

### For Gemini:
```bash
GEMINI_API_KEY=your-actual-gemini-api-key
GEMINI_API_BASE=https://generativelanguage.googleapis.com/v1beta    # Default
```

### For Moonshot:
```bash
MOONSHOT_API_KEY=sk-your-actual-moonshot-key
MOONSHOT_API_BASE=https://api.moonshot.cn/v1
```

### For ZAI:
```bash
ZAI_API_KEY=sk-your-actual-zai-key
ZAI_API_BASE=https://api.z.ai/v1
ZAI_MODEL=gpt-4-turbo    # Only needed if your provider requires a specific model param
```

## Optional Variables

```bash
# Timing
LLM_TIMEOUT=60
LLM_MAX_RETRIES=3

# Generation settings
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=500

# Debug
DEBUG=false

# Caching
CACHE_DIR=~/.cache/context-generator
```

## n8n Integration (Optional)

```bash
N8N_HOST=https://n8n.homelab.martinmayday.com
N8N_WEBHOOK_AUTH_HEADER=X-N8N-Auth-Token
N8N_WEBHOOK_TOKEN=your-token
N8N_WEBHOOK_ON_COMPLETE=https://n8n.homelab.martinmayday.com/webhook/context-generator/complete
N8N_WEBHOOK_ON_ERROR=https://n8n.homelab.martinmayday.com/webhook/context-generator/error
N8N_API_KEY=your-api-key
```

## Verify Your Configuration

Run this to test:

```bash
cd /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/tmp/context_generator
source .env
echo $CONTEXT_GENERATOR_MODEL
echo $OPENROUTER_API_KEY | cut -c1-10

# If those show your values, then try:
python -m context_generator ./context_generator --dry-run --verbose
```

## Common Mistakes

❌ **Wrong** - Using multiple model variables:
```bash
# Don't do this
CONTEXT_GENERATOR_MODEL=ollama/llama3.2
OPENROUTER_MODEL=anthropic/claude-3-haiku
GEMINI_MODEL=gemini-1.5-flash
```

✅ **Right** - Use only ONE:
```bash
# Do this
CONTEXT_GENERATOR_MODEL=openrouter/anthropic/claude-3-haiku
OPENROUTER_API_KEY=sk-your-key
```

❌ **Wrong** - Missing provider in model string:
```bash
# Don't do this
CONTEXT_GENERATOR_MODEL=claude-3-haiku
```

✅ **Right** - Include provider prefix:
```bash
# Do this
CONTEXT_GENERATOR_MODEL=openrouter/anthropic/claude-3-haiku
```

## What Works Now

After the fixes:
1. ✅ CLI loads `.env` automatically
2. ✅ Uses `CONTEXT_GENERATOR_MODEL` from environment
3. ✅ Command line `--model` overrides environment
4. ✅ Provider-specific env vars (API keys, hosts) are used
5. ✅ `offline` mode works without any API keys

## Quick Test

```bash
cd /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/tmp/context_generator

# Test offline (no config needed)
python -m context_generator ./ --dry-run --offline

# Test with your .env
python -m context_generator ./ --dry-run
```
