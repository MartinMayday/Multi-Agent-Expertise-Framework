from typing import Any, Dict, Optional, List
from pathlib import Path


class AgentRegistry:
    """Central registry for discovering and managing agents."""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.adapters: Dict[str, str] = {}  # name -> adapter_type
    
    def register(self, name: str, agent_class: type, adapter_type: str = "pydantic_ai") -> None:
        """Register an agent."""
        self.agents[name] = agent_class
        self.adapters[name] = adapter_type
    
    def get_agent(self, name: str) -> Optional[Any]:
        """Get agent class by name."""
        return self.agents.get(name)
    
    def get_adapter(self, name: str) -> Optional[str]:
        """Get agent's adapter type."""
        return self.adapters.get(name)
    
    def list_agents(self) -> List[str]:
        """List all registered agents."""
        return list(self.agents.keys())
    
    def load_from_directory(self, agents_dir: Path) -> None:
        """Discover agents from a directory structure."""
        agents_dir = Path(agents_dir)
        if not agents_dir.exists():
            return
        
        # Scan for AGENTS.md files
        for agents_file in agents_dir.glob("**/AGENTS.md"):
            # Parse and register agents from AGENTS.md
            # This is a placeholder - actual implementation would parse YAML/Markdown
            pass


# Global registry instance
_global_registry = AgentRegistry()


def register_agent(name: str, agent_class: type, adapter_type: str = "pydantic_ai") -> None:
    """Register an agent globally."""
    _global_registry.register(name, agent_class, adapter_type)


def get_agent(name: str) -> Optional[Any]:
    """Get agent from global registry."""
    return _global_registry.get_agent(name)


def list_agents() -> List[str]:
    """List all registered agents."""
    return _global_registry.list_agents()
