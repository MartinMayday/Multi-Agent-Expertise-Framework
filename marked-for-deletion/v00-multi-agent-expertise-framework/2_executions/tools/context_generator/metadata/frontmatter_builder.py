"""Build YAML frontmatter for file metadata."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field, asdict
from typing import Optional
import yaml

logger = logging.getLogger(__name__)


@dataclass
class FrontmatterMetadata:
    """Complete frontmatter metadata for a file."""
    id: str
    path: str
    tokens: int
    chunk_type: str
    keywords: list[str] = field(default_factory=list)
    priority: str = "medium"
    summary: str = ""
    when_to_load: list[str] = field(default_factory=list)
    retrieval_triggers: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    search_hints: dict = field(default_factory=dict)


class FrontmatterBuilder:
    """Builds YAML frontmatter for files."""

    CHUNK_TYPES = {
        "contract": "System rules, guardrails, validation contracts",
        "methodology": "Frameworks, patterns, procedures, templates",
        "architecture": "System design, components, interfaces, dependencies",
        "execution": "Implementation, code, workflows, runbooks",
        "reference": "Definitions, glossaries, lookups, indexes",
    }

    def __init__(self):
        """Initialize frontmatter builder."""
        pass

    def build(
        self,
        file_id: str,
        file_path: str,
        tokens: int,
        chunk_type: str,
        keywords: list[str] | None = None,
        summary: str = "",
        when_to_load: list[str] | None = None,
        retrieval_triggers: list[str] | None = None,
        dependencies: list[str] | None = None,
        priority: str = "medium",
    ) -> str:
        """
        Build YAML frontmatter block.

        Returns:
            YAML frontmatter string
        """
        metadata = FrontmatterMetadata(
            id=file_id,
            path=file_path,
            tokens=tokens,
            chunk_type=chunk_type,
            keywords=keywords or [],
            priority=priority,
            summary=summary,
            when_to_load=when_to_load or [],
            retrieval_triggers=retrieval_triggers or [],
            dependencies=dependencies or [],
            search_hints={
                "bm25_terms": [kw for kw in (keywords or []) if len(kw) > 3],
                "semantic_signals": [],
            },
        )

        # Convert to dict and filter empty values
        data = asdict(metadata)
        data = {k: v for k, v in data.items() if v}

        # Build YAML frontmatter
        yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False)
        return f"---\n{yaml_str}---\n"

    def validate_chunk_type(self, chunk_type: str) -> bool:
        """Validate chunk_type is recognized."""
        return chunk_type in self.CHUNK_TYPES

    def classify_by_rules(self, file_path: str, content_sample: str) -> str:
        """
        Classify chunk_type using heuristic rules.

        Returns:
            One of: contract, methodology, architecture, execution, reference
        """
        path_lower = file_path.lower()
        content_lower = content_sample.lower()

        # Contract detection
        if any(x in path_lower for x in ["contract", "guardrail", "directive", "rules"]):
            return "contract"
        if any(x in content_lower for x in ["must enforce", "guardrail", "shall not", "forbidden"]):
            return "contract"

        # Methodology detection
        if any(x in path_lower for x in ["framework", "pattern", "template", "procedure"]):
            return "methodology"
        if any(x in content_lower for x in ["framework", "pattern", "methodology", "procedure"]):
            return "methodology"

        # Architecture detection
        if any(x in path_lower for x in ["arch", "design", "system", "component"]):
            return "architecture"
        if any(x in content_lower for x in ["architecture", "component", "interface", "dependency graph"]):
            return "architecture"

        # Execution detection
        if any(x in path_lower for x in ["exec", "script", "workflow", "implementation", "code"]):
            return "execution"
        if any(x in content_lower for x in ["def ", "class ", "function", "import ", "implementation"]):
            return "execution"

        # Default to reference
        return "reference"

    def prioritize(self, tokens: int, dependency_count: int = 0) -> str:
        """
        Prioritize file based on size and dependencies.

        Args:
            tokens: Estimated token count
            dependency_count: Number of files depending on this

        Returns:
            One of: high, medium, low
        """
        # High: Core contract/architecture (2K+ tokens or many deps)
        if tokens > 2000 or dependency_count > 3:
            return "high"

        # Medium: Normal files
        if tokens > 500 or dependency_count > 0:
            return "medium"

        # Low: Small, isolated files
        return "low"
