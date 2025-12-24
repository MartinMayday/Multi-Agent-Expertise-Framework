# Multi-Agent Framework Integration

This directory contains pluggable adapters for integrating different multi-agent frameworks.

## Supported Frameworks

- **PydanticAI** (recommended): Built-in support for Claude models
- **CrewAI**: Team of cooperative agents
- **Claude Agent SDK**: Official Anthropic agent framework
- **PraisonAI**: Production-ready agent orchestration
- **Claude-Flow**: Flow-based agent coordination

## Base Interface

All agents implement `BaseAgent` (see `base_agent.py`):

```python
class BaseAgent:
    async def invoke(self, prompt: str, context: dict) -> str:
        """Execute agent with context."""
    
    async def stream(self, prompt: str) -> AsyncIterator[str]:
        """Stream responses."""
```

## Quick Start

### Using PydanticAI (Recommended)

```python
from src.agents.adapters.pydantic_ai import PydanticAIAgent

agent = PydanticAIAgent(
    name="database-expert",
    model="claude-3-5-sonnet-20241022",
    system_prompt="You are a database expert..."
)

result = await agent.invoke("Design a schema for...")
```

### Using CrewAI

```python
from src.agents.adapters.crew_ai import CrewAIAdapter

crew = CrewAIAdapter(
    agents=[...],
    tasks=[...]
)

result = await crew.invoke("Plan the project")
```

## Architecture

```
interfaces/
├── base_agent.py          # Abstract base class
└── agent_registry.py      # Agent discovery & management

adapters/
├── pydantic_ai.py         # PydanticAI wrapper
├── crew_ai.py             # CrewAI wrapper
├── claude_sdk.py          # Official Claude Agent SDK
├── claude_flow.py         # Flow-based coordination
└── praison_ai.py          # PraisonAI wrapper
```

## Adding a New Framework

1. Create a new adapter file in `adapters/`
2. Implement `BaseAgent` interface
3. Register in `agent_registry.py`
4. Add configuration in environment/config

## Status

- [x] Base interface defined
- [x] PydanticAI adapter (stub)
- [x] CrewAI adapter (stub)
- [x] Claude Agent SDK adapter (stub)
- [x] PraisonAI adapter (stub)
- [x] Claude-Flow adapter (stub)
- [ ] Full implementations (pending framework selection)
