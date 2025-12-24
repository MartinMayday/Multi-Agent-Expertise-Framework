"""
LLM-enhanced executors that use directives/SOPs for predictable output.

Each executor:
1. Loads its directive YAML
2. Fills template with static analysis data
3. Calls LLM with structured prompt
4. Validates and cleans output
5. Falls back to static generation on failure
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .directive_loader import DirectiveLoader, get_default_loader
from .llm_client import BaseLLMClient, LLMResponse

logger = logging.getLogger(__name__)


@dataclass
class ExecutorResult:
    """Result from an executor."""
    text: str
    source: str
    success: bool
    tokens_used: int = 0
    error: Optional[str] = None


class BaseExecutor:
    """Base class for SOP-driven executors."""
    
    directive_name: str = ""
    
    def __init__(self, llm_client: BaseLLMClient, loader: Optional[DirectiveLoader] = None):
        self.llm_client = llm_client
        self.loader = loader or get_default_loader()
        self._directive = None
    
    @property
    def directive(self):
        if self._directive is None:
            self._directive = self.loader.load(self.directive_name)
        return self._directive
    
    def execute(self, **kwargs) -> ExecutorResult:
        """Execute the directive with provided inputs."""
        prompt = self.directive.render_prompt(**kwargs)
        
        response = self.llm_client.complete(
            prompt=prompt,
            max_tokens=self.directive.validation.max_tokens,
            temperature=0.3
        )
        
        if not response.success:
            logger.warning(f"LLM call failed: {response.error}")
            fallback = self.get_fallback(**kwargs)
            return ExecutorResult(
                text=fallback,
                source="fallback",
                success=False,
                error=response.error
            )
        
        cleaned = self.directive.clean_output(response.text)
        is_valid, validation_error = self.directive.validate_output(cleaned)
        
        if not is_valid:
            logger.warning(f"Output validation failed: {validation_error}")
            fallback = self.get_fallback(**kwargs)
            return ExecutorResult(
                text=fallback,
                source="fallback",
                success=False,
                tokens_used=response.tokens_used,
                error=validation_error
            )
        
        return ExecutorResult(
            text=cleaned,
            source="llm",
            success=True,
            tokens_used=response.tokens_used
        )
    
    def get_fallback(self, **kwargs) -> str:
        """Generate fallback output when LLM is unavailable or fails."""
        raise NotImplementedError


class FolderSummarizer(BaseExecutor):
    """Generates folder purpose statements."""
    
    directive_name = "summarize_folder"
    
    def summarize(
        self,
        folder_name: str,
        file_list: list[str],
        symbol_summary: str,
        readme_content: Optional[str] = None
    ) -> ExecutorResult:
        return self.execute(
            folder_name=folder_name,
            file_list=file_list,
            symbol_summary=symbol_summary,
            readme_content=readme_content or "N/A"
        )
    
    def get_fallback(self, **kwargs) -> str:
        folder_name = kwargs.get("folder_name", "unknown")
        file_list = kwargs.get("file_list", [])
        symbol_summary = kwargs.get("symbol_summary", "")
        
        if symbol_summary:
            return f"{folder_name} - {symbol_summary[:100]}"
        
        count = len(file_list) if isinstance(file_list, list) else 0
        return f"{folder_name} - contains {count} source files"


class FileDescriber(BaseExecutor):
    """Generates file descriptions."""
    
    directive_name = "describe_file"
    
    def describe(
        self,
        filename: str,
        language: str,
        symbols: list[str],
        first_lines: str,
        docstring: Optional[str] = None
    ) -> ExecutorResult:
        return self.execute(
            filename=filename,
            language=language,
            symbols=symbols,
            first_lines=first_lines,
            docstring=docstring or "N/A"
        )
    
    def get_fallback(self, **kwargs) -> str:
        docstring = kwargs.get("docstring")
        if docstring:
            first_line = docstring.split("\n")[0].strip()
            if first_line:
                return first_line[:150]
        
        symbols = kwargs.get("symbols", [])
        if symbols:
            return f"Contains {symbols[0]}" + (f" and {len(symbols)-1} more" if len(symbols) > 1 else "")
        
        return "Source file"


class DependencyInferrer(BaseExecutor):
    """Generates semantic dependency descriptions."""
    
    directive_name = "infer_dependencies"
    
    def infer(
        self,
        folder_name: str,
        folder_purpose: str,
        depends_on: list[str],
        used_by: list[str],
        import_examples: list[str]
    ) -> ExecutorResult:
        return self.execute(
            folder_name=folder_name,
            folder_purpose=folder_purpose,
            depends_on=depends_on,
            used_by=used_by,
            import_examples=import_examples
        )
    
    def get_fallback(self, **kwargs) -> str:
        depends_on = kwargs.get("depends_on", [])
        used_by = kwargs.get("used_by", [])
        
        parts = []
        if depends_on:
            parts.append(f"Depends on: {', '.join(depends_on[:3])}")
        if used_by:
            parts.append(f"Used by: {', '.join(used_by[:3])}")
        
        return ". ".join(parts) if parts else "No significant dependencies detected."
