# Environment Configuration Setup

This guide explains how to configure the context generator for different LLM providers.

## Quick Start (Offline Mode - No Setup Required)

The tool works with **zero LLM configuration** for static analysis:

```bash
# Uses only AST parsing + regex extraction
python -m context_generator ./my-repo --offline
```

## Production Setup: Choose Your LLM Provider

### 1. Create `.env` file

```bash
cp env.example .env
```

**IMPORTANT**: `.env` contains API keys and secrets
- Never commit `.env` to version control
- Add `.env` to `.gitignore`
- Keep secure (file permissions: `chmod 600 .env`)

### 2. Pick One Provider and Configure

#### Option A: Ollama (Local, Free, Private)

**Best for**: Privacy, offline work, cost-free deployments

1. Install Ollama: https://ollama.ai
2. Pull a model:
   ```bash
   ollama pull llama3.2      # 3.2B, balanced
   ollama pull mistral       # 7B, strong reasoning
   ollama pull codellama:7b  # 7B, code-focused
   ```
3. Run Ollama server:
   ```bash
   ollama serve
   ```
4. Configure `.env`:
   ```bash
   CONTEXT_GENERATOR_MODEL=ollama/llama3.2
   OLLAMA_HOST=http://localhost:11434
   ```
5. Test:
   ```bash
   python -m context_generator ./my-repo
   ```

---

#### Option B: LM Studio (Local GUI, Free, Private)

**Best for**: Non-technical users, GUI model management, experimental features

1. Download: https://lmstudio.ai
2. Launch LM Studio app
3. Search and load a model (e.g., "TheBloke/Llama-2-7B-Chat-GGUF")
4. Click "Developer Console" (gear icon)
5. Click "Start Server" (default port 1234)
6. Configure `.env`:
   ```bash
   CONTEXT_GENERATOR_MODEL=lmstudio/TheBloke/Llama-2-7B-Chat-GGUF
   LMSTUDIO_HOST=http://localhost:1234
   LMSTUDIO_API_KEY=lm-studio
   ```
7. Test:
   ```bash
   python -m context_generator ./my-repo
   ```

---

#### Option C: OpenRouter (Cloud, 200+ Models, $0.50-15/1M tokens)

**Best for**: Best model selection, easy scaling, multi-provider access

1. Get API key: https://openrouter.ai/keys
2. Pick a model:
   - **Fastest/Cheapest**: `google/gemini-flash-1.5` (~$0.10/1M input)
   - **Balanced**: `anthropic/claude-3-haiku` (~$0.80/1M input)
   - **Best Quality**: `anthropic/claude-3.5-sonnet` (~$3/1M input)
3. Configure `.env`:
   ```bash
   CONTEXT_GENERATOR_MODEL=openrouter/anthropic/claude-3-haiku
   OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key
   ```
4. Test:
   ```bash
   python -m context_generator ./my-repo
   ```

---

#### Option D: Google Gemini (Cloud, 1M-2M context, $0.075-1.50/1M tokens)

**Best for**: Large context windows, free tier available

1. Get API key: https://aistudio.google.com/apikey
2. Pick a model:
   - **Free tier**: `gemini-1.5-flash` (15 req/min, 1M tokens/day)
   - **Paid**: `gemini-1.5-pro` (2M context window)
3. Configure `.env`:
   ```bash
   CONTEXT_GENERATOR_MODEL=gemini/gemini-1.5-flash
   GEMINI_API_KEY=your-actual-gemini-api-key
   ```
4. Test:
   ```bash
   python -m context_generator ./my-repo
   ```

---

#### Option E: Moonshot AI (Cloud, China-optimized, 8K-128K context)

**Best for**: China-based users, large context windows, competitive pricing

1. Get API key: https://platform.moonshot.cn/console/api-keys
2. Pick a model:
   - `moonshot-v1-8k` (8K context)
   - `moonshot-v1-32k` (32K context)
   - `moonshot-v1-128k` (128K context)
3. Configure `.env`:
   ```bash
   CONTEXT_GENERATOR_MODEL=moonshot/moonshot-v1-8k
   MOONSHOT_API_KEY=sk-your-actual-moonshot-api-key
   MOONSHOT_API_BASE=https://api.moonshot.cn/v1
   ```
4. Test:
   ```bash
   python -m context_generator ./my-repo
   ```

---

#### Option F: ZAI Codingplan (Enterprise, Custom Endpoints)

**Best for**: Enterprise deployments, custom models, dedicated support

1. Contact ZAI for credentials: https://platform.zai.ai
2. Get your API endpoint and model names
3. Configure `.env`:
   ```bash
   CONTEXT_GENERATOR_MODEL=zai/your-enterprise-model
   ZAI_API_KEY=sk-your-actual-zai-api-key
   ZAI_API_BASE=https://api.z.ai/v1
   ZAI_MODEL=your-enterprise-model
   ```
4. Test:
   ```bash
   python -m context_generator ./my-repo
   ```

---

## Usage Examples

### Generate CLAUDE.md files with your chosen provider

```bash
# Using Ollama (local)
python -m context_generator ./my-repo --model ollama/llama3.2

# Using OpenRouter (cloud)
python -m context_generator ./my-repo --model openrouter/anthropic/claude-3-haiku

# Using Gemini (cloud)
python -m context_generator ./my-repo --model gemini/gemini-1.5-flash

# Static analysis only (no LLM calls)
python -m context_generator ./my-repo --offline
```

### Advanced options

```bash
# Preview without writing files
python -m context_generator ./my-repo --dry-run

# Limit folder depth
python -m context_generator ./my-repo --depth 5

# Minimum files per folder
python -m context_generator ./my-repo --min-files 3

# Enable verbose logging
python -m context_generator ./my-repo --verbose
```

---

## Cost Comparison

| Provider | Cost | Model | Speed | Quality |
|----------|------|-------|-------|---------|
| **Ollama** | Free | llama3.2 3B | Fast | Good |
| **Ollama** | Free | llama3.1 70B | Slow | Excellent |
| **LM Studio** | Free | Any local model | Depends | Depends |
| **OpenRouter** | $0.10/1M | Gemini Flash | Very Fast | Good |
| **OpenRouter** | $0.80/1M | Claude 3 Haiku | Fast | Very Good |
| **OpenRouter** | $3/1M | Claude 3.5 Sonnet | Medium | Excellent |
| **Gemini** | $0.075/1M | Gemini 1.5 Flash | Very Fast | Good |
| **Gemini** | Free tier | Gemini 1.5 Flash | Very Fast | Good |
| **Moonshot** | $/M tokens | moonshot-v1-8k | Fast | Good |

---

## Troubleshooting

### "Module not found" error

Ensure installation:
```bash
cd tmp/context_generator
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### LLM connection failed

1. Check that the LLM service is running:
   - **Ollama**: `curl http://localhost:11434/api/tags`
   - **LM Studio**: Open the Developer Console
   - **Cloud APIs**: Check your API key is correct

2. Verify environment variables:
   ```bash
   source .env
   echo $OLLAMA_HOST  # or $OPENROUTER_API_KEY, etc.
   ```

### API key errors

- Ensure no spaces or extra characters around the API key
- Check the key is for the correct provider
- Verify the key has the necessary permissions

### Slow generation

- Switch to a smaller/faster model (e.g., `llama3.2` → `llama3.2:1b`)
- Use `--offline` flag to skip LLM calls
- Reduce token limits: `LLM_MAX_TOKENS=200`

---

## Security Best Practices

1. **Never commit `.env`**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Keep API keys secure**
   ```bash
   chmod 600 .env
   ```

3. **Use provider credentials wisely**
   - OpenRouter: Rotate API keys regularly
   - Gemini: Use restrictive API key restrictions if available
   - Moonshot: Use separate keys for dev/production

4. **Monitor API usage**
   - OpenRouter: Check usage dashboard
   - Gemini: Monitor quota in Cloud Console
   - Moonshot: Check balance in platform dashboard

---

## Next Steps

- [View model benchmarks](https://lmarena.ai/)
- [OpenRouter catalog](https://openrouter.ai/)
- [Ollama library](https://ollama.ai/library)
- [LM Studio docs](https://lmstudio.ai/)
- [Claude Code memory system](https://code.claude.com/docs/en/memory)
