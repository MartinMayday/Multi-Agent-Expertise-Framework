"""
LLM Client abstraction supporting multiple providers.

Supported providers:
    - ollama: Local Ollama server
    - lmstudio: Local LM Studio server (OpenAI-compatible)
    - openrouter: OpenRouter API (multi-provider cloud)
    - gemini: Google Gemini API
    - moonshot: Moonshot AI API (China)
    - zai: ZAI Codingplan API

Usage:
    client = LLMClient.from_model_string("openrouter/anthropic/claude-3-haiku")
    client = LLMClient.from_model_string("ollama/llama3")
    client = LLMClient.from_model_string("gemini/gemini-1.5-flash")
    
    response = client.complete(prompt, max_tokens=100)
"""

from __future__ import annotations

import os
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Standardized LLM response."""
    text: str
    model: str
    tokens_used: int
    success: bool
    error: Optional[str] = None


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.3) -> LLMResponse:
        """Generate completion for the given prompt."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM service is available."""
        pass


class OpenRouterClient(BaseLLMClient):
    """OpenRouter API client."""
    
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    def __init__(self, model: str, api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        self._client = httpx.Client(timeout=60.0)
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.3) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(
                text="",
                model=self.model,
                tokens_used=0,
                success=False,
                error="OPENROUTER_API_KEY not set"
            )
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/context-generator",
            "X-Title": "Context Generator"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self._client.post(self.BASE_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            text = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            
            return LLMResponse(
                text=text.strip(),
                model=self.model,
                tokens_used=tokens,
                success=True
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter API error: {e.response.status_code}")
            return LLMResponse(
                text="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=f"HTTP {e.response.status_code}: {e.response.text[:200]}"
            )
        except Exception as e:
            logger.error(f"OpenRouter request failed: {e}")
            return LLMResponse(
                text="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=str(e)
            )


class OllamaClient(BaseLLMClient):
    """Ollama local model client."""
    
    DEFAULT_HOST = "http://localhost:11434"
    
    def __init__(self, model: str, host: Optional[str] = None):
        self.model = model
        self.host = host or os.environ.get("OLLAMA_HOST", self.DEFAULT_HOST)
        self._client = httpx.Client(timeout=120.0)
    
    def is_available(self) -> bool:
        try:
            response = self._client.get(f"{self.host}/api/tags")
            return response.status_code == 200
        except Exception:
            return False
    
    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.3) -> LLMResponse:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }
        
        try:
            response = self._client.post(f"{self.host}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()
            
            text = data.get("response", "")
            tokens = data.get("eval_count", 0) + data.get("prompt_eval_count", 0)
            
            return LLMResponse(
                text=text.strip(),
                model=self.model,
                tokens_used=tokens,
                success=True
            )
        except httpx.ConnectError:
            return LLMResponse(
                text="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=f"Cannot connect to Ollama at {self.host}"
            )
        except Exception as e:
            logger.error(f"Ollama request failed: {e}")
            return LLMResponse(
                text="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=str(e)
            )


class LMStudioClient(BaseLLMClient):
    """LM Studio local server client (OpenAI-compatible API)."""
    
    DEFAULT_HOST = "http://localhost:1234"
    
    def __init__(self, model: str, host: Optional[str] = None):
        self.model = model
        self.host = host or os.environ.get("LMSTUDIO_HOST", self.DEFAULT_HOST)
        self.api_key = os.environ.get("LMSTUDIO_API_KEY", "lm-studio")
        self._client = httpx.Client(timeout=120.0)
    
    def is_available(self) -> bool:
        try:
            response = self._client.get(f"{self.host}/v1/models")
            return response.status_code == 200
        except Exception:
            return False
    
    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.3) -> LLMResponse:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self._client.post(f"{self.host}/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            text = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            
            return LLMResponse(text=text.strip(), model=self.model, tokens_used=tokens, success=True)
        except httpx.ConnectError:
            return LLMResponse(text="", model=self.model, tokens_used=0, success=False,
                             error=f"Cannot connect to LM Studio at {self.host}")
        except Exception as e:
            logger.error(f"LM Studio request failed: {e}")
            return LLMResponse(text="", model=self.model, tokens_used=0, success=False, error=str(e))


class GeminiClient(BaseLLMClient):
    """Google Gemini API client."""
    
    DEFAULT_BASE = "https://generativelanguage.googleapis.com/v1beta"
    
    def __init__(self, model: str, api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.base_url = os.environ.get("GEMINI_API_BASE", self.DEFAULT_BASE)
        self._client = httpx.Client(timeout=60.0)
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.3) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(text="", model=self.model, tokens_used=0, success=False,
                             error="GEMINI_API_KEY not set")
        
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature
            }
        }
        
        try:
            response = self._client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            tokens = data.get("usageMetadata", {}).get("totalTokenCount", 0)
            
            return LLMResponse(text=text.strip(), model=self.model, tokens_used=tokens, success=True)
        except Exception as e:
            logger.error(f"Gemini request failed: {e}")
            return LLMResponse(text="", model=self.model, tokens_used=0, success=False, error=str(e))


class MoonshotClient(BaseLLMClient):
    """Moonshot AI API client (China)."""
    
    DEFAULT_BASE = "https://api.moonshot.cn/v1"
    
    def __init__(self, model: str, api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.environ.get("MOONSHOT_API_KEY")
        self.base_url = os.environ.get("MOONSHOT_API_BASE", self.DEFAULT_BASE)
        self._client = httpx.Client(timeout=60.0)
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.3) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(text="", model=self.model, tokens_used=0, success=False,
                             error="MOONSHOT_API_KEY not set")
        
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self._client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            text = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            
            return LLMResponse(text=text.strip(), model=self.model, tokens_used=tokens, success=True)
        except Exception as e:
            logger.error(f"Moonshot request failed: {e}")
            return LLMResponse(text="", model=self.model, tokens_used=0, success=False, error=str(e))


class ZAIClient(BaseLLMClient):
    """ZAI Codingplan API client."""
    
    def __init__(self, model: str, api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.environ.get("ZAI_API_KEY")
        self.base_url = os.environ.get("ZAI_API_BASE", "https://api.zai.codingplan.io/v1")
        self._client = httpx.Client(timeout=60.0)
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.3) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(text="", model=self.model, tokens_used=0, success=False,
                             error="ZAI_API_KEY not set")
        
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self._client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            text = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            
            return LLMResponse(text=text.strip(), model=self.model, tokens_used=tokens, success=True)
        except Exception as e:
            logger.error(f"ZAI request failed: {e}")
            return LLMResponse(text="", model=self.model, tokens_used=0, success=False, error=str(e))


class OfflineClient(BaseLLMClient):
    """Offline fallback client that returns empty responses."""
    
    def __init__(self):
        pass
    
    def is_available(self) -> bool:
        return True
    
    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.3) -> LLMResponse:
        return LLMResponse(
            text="",
            model="offline",
            tokens_used=0,
            success=False,
            error="Running in offline mode"
        )


class LLMClient:
    """Factory for creating LLM clients from model strings."""
    
    @staticmethod
    def from_model_string(model_string: str, offline: bool = False) -> BaseLLMClient:
        """
        Create an LLM client from a model string.
        
        Formats:
            - "ollama/<model>" -> OllamaClient (local)
            - "lmstudio/<model>" -> LMStudioClient (local, OpenAI-compatible)
            - "openrouter/<model>" -> OpenRouterClient (cloud, multi-provider)
            - "gemini/<model>" -> GeminiClient (Google cloud)
            - "moonshot/<model>" -> MoonshotClient (China cloud)
            - "zai/<model>" -> ZAIClient (custom/enterprise)
            - "offline" -> OfflineClient (no LLM)
        
        Examples:
            - "ollama/llama3.2"
            - "ollama/codellama:7b"
            - "lmstudio/local-model"
            - "openrouter/anthropic/claude-3-haiku"
            - "openrouter/google/gemini-flash-1.5"
            - "gemini/gemini-1.5-flash"
            - "moonshot/moonshot-v1-8k"
            - "zai/codingplan-v1"
        """
        if offline or model_string.lower() == "offline":
            return OfflineClient()
        
        parts = model_string.split("/", 1)
        if len(parts) < 2:
            raise ValueError(f"Invalid model string: {model_string}. Expected 'provider/model'")
        
        provider = parts[0].lower()
        model = parts[1]
        
        providers = {
            "ollama": OllamaClient,
            "lmstudio": LMStudioClient,
            "openrouter": OpenRouterClient,
            "gemini": GeminiClient,
            "moonshot": MoonshotClient,
            "zai": ZAIClient,
        }
        
        if provider not in providers:
            supported = ", ".join(providers.keys())
            raise ValueError(f"Unknown provider: {provider}. Supported: {supported}")
        
        return providers[provider](model=model)
