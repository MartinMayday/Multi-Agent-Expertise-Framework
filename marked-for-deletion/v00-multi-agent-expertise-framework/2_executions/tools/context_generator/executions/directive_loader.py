"""
Directive loader for YAML SOP files.

Directives define structured templates for LLM tasks with:
- Input schema with placeholders
- Output format and validation rules
- Correct and wrong examples for few-shot prompting
"""

from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

logger = logging.getLogger(__name__)


@dataclass
class OutputValidation:
    """Validation rules for LLM output."""
    max_tokens: int = 500
    max_length: Optional[int] = None
    must_not_contain: list[str] = field(default_factory=list)
    must_contain: list[str] = field(default_factory=list)
    must_be_single_line: bool = False
    strip_markdown: bool = False


@dataclass
class Directive:
    """A loaded directive/SOP for LLM tasks."""
    name: str
    version: str
    description: str
    template: str
    inputs: list[dict[str, str]]
    output_type: str
    output_format: str
    validation: OutputValidation
    correct_examples: list[str] = field(default_factory=list)
    wrong_examples: list[str] = field(default_factory=list)
    
    def render_prompt(self, **kwargs) -> str:
        """
        Render the prompt template with provided variables.
        
        Uses simple {variable} placeholder substitution.
        """
        prompt = self.template
        for key, value in kwargs.items():
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            placeholder = "{" + key + "}"
            prompt = prompt.replace(placeholder, str(value) if value else "N/A")
        
        missing = re.findall(r'\{(\w+)\}', prompt)
        if missing:
            logger.warning(f"Directive '{self.name}' has unfilled placeholders: {missing}")
        
        return prompt
    
    def validate_output(self, output: str) -> tuple[bool, Optional[str]]:
        """
        Validate LLM output against directive rules.
        
        Returns (is_valid, error_message).
        """
        if not output:
            return False, "Output is empty"
        
        if self.validation.max_length and len(output) > self.validation.max_length:
            return False, f"Output exceeds max length: {len(output)} > {self.validation.max_length}"
        
        if self.validation.must_be_single_line and "\n" in output.strip():
            return False, "Output must be single line"
        
        for forbidden in self.validation.must_not_contain:
            if forbidden in output:
                return False, f"Output contains forbidden pattern: '{forbidden}'"
        
        for required in self.validation.must_contain:
            if required not in output:
                return False, f"Output missing required pattern: '{required}'"
        
        return True, None
    
    def clean_output(self, output: str) -> str:
        """Clean and normalize LLM output."""
        result = output.strip()
        
        if self.validation.strip_markdown:
            result = re.sub(r'^#+\s*', '', result)
            result = re.sub(r'\*\*([^*]+)\*\*', r'\1', result)
            result = re.sub(r'`([^`]+)`', r'\1', result)
        
        if self.validation.must_be_single_line:
            result = result.replace("\n", " ").strip()
            result = re.sub(r'\s+', ' ', result)
        
        return result


class DirectiveLoader:
    """Loads and manages directives from YAML files."""
    
    def __init__(self, directives_dir: Path):
        self.directives_dir = Path(directives_dir)
        self._cache: dict[str, Directive] = {}
    
    def load(self, name: str) -> Directive:
        """Load a directive by name (filename without .yaml extension)."""
        if name in self._cache:
            return self._cache[name]
        
        yaml_path = self.directives_dir / f"{name}.yaml"
        if not yaml_path.exists():
            raise FileNotFoundError(f"Directive not found: {yaml_path}")
        
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        directive = self._parse_directive(data)
        self._cache[name] = directive
        return directive
    
    def _parse_directive(self, data: dict[str, Any]) -> Directive:
        """Parse directive data from YAML."""
        output_config = data.get("output", {})
        validation_config = data.get("validation", {})
        
        validation = OutputValidation(
            max_tokens=validation_config.get("max_tokens", 500),
            max_length=output_config.get("max_length"),
            must_not_contain=validation_config.get("must_not_contain", []),
            must_contain=validation_config.get("must_contain", []),
            must_be_single_line=validation_config.get("must_be_single_line", False),
            strip_markdown=validation_config.get("strip_markdown", False)
        )
        
        correct_examples = []
        wrong_examples = []
        template = data.get("template", "")
        
        if "CORRECT EXAMPLES:" in template:
            parts = template.split("CORRECT EXAMPLES:")
            if len(parts) > 1:
                examples_section = parts[1]
                if "WRONG EXAMPLES:" in examples_section:
                    correct_part, wrong_part = examples_section.split("WRONG EXAMPLES:", 1)
                    correct_examples = self._parse_examples(correct_part)
                    wrong_examples = self._parse_examples(wrong_part)
                else:
                    correct_examples = self._parse_examples(examples_section)
        
        return Directive(
            name=data.get("name", "unknown"),
            version=data.get("version", "1.0"),
            description=data.get("description", ""),
            template=template,
            inputs=data.get("inputs", []),
            output_type=output_config.get("type", "string"),
            output_format=output_config.get("format", ""),
            validation=validation,
            correct_examples=correct_examples,
            wrong_examples=wrong_examples
        )
    
    def _parse_examples(self, text: str) -> list[str]:
        """Extract examples from template text (lines starting with -)."""
        examples = []
        for line in text.strip().split("\n"):
            line = line.strip()
            if line.startswith("- "):
                example = line[2:].strip().strip('"').strip("'")
                if example:
                    examples.append(example)
        return examples
    
    def list_available(self) -> list[str]:
        """List all available directive names."""
        if not self.directives_dir.exists():
            return []
        return [p.stem for p in self.directives_dir.glob("*.yaml")]


def get_default_loader() -> DirectiveLoader:
    """Get a loader for the built-in directives."""
    directives_dir = Path(__file__).parent.parent / "directives"
    return DirectiveLoader(directives_dir)
