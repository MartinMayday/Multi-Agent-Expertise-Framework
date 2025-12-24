from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, Optional


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, name: str, system_prompt: str = ""):
        self.name = name
        self.system_prompt = system_prompt
    
    @abstractmethod
    async def invoke(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Execute agent with prompt and optional context.
        
        Args:
            prompt: User input or task description
            context: Optional dictionary with task context, memory, tools, etc.
        
        Returns:
            Agent response as string
        """
        pass
    
    @abstractmethod
    async def stream(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> AsyncIterator[str]:
        """Stream agent responses token-by-token.
        
        Args:
            prompt: User input or task description
            context: Optional dictionary with task context
        
        Yields:
            Streamed response tokens
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent metadata."""
        return {
            "name": self.name,
            "system_prompt": self.system_prompt
        }
