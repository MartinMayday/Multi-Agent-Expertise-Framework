"""Classify file intent and generate when_to_load conditions."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class IntentResult:
    """File intent classification result."""
    chunk_type: str
    when_to_load: list[str]
    retrieval_triggers: list[str]


class IntentClassifier:
    """Classify file intent and generate context loading conditions."""

    # Pattern-based classification rules
    CONTRACT_PATTERNS = {
        "keywords": ["contract", "guardrail", "enforce", "mandate", "rule", "constraint", "forbidden"],
        "content": ["must enforce", "shall not", "guardrail", "constraint", "forbidden action", "validation"],
    }

    METHODOLOGY_PATTERNS = {
        "keywords": ["framework", "pattern", "template", "procedure", "methodology", "approach", "guide"],
        "content": ["framework", "pattern", "methodology", "step-by-step", "best practice"],
    }

    ARCHITECTURE_PATTERNS = {
        "keywords": ["architecture", "design", "component", "system", "interface", "module", "structure"],
        "content": ["architecture", "component", "interface", "dependency", "system design"],
    }

    EXECUTION_PATTERNS = {
        "keywords": ["exec", "script", "workflow", "implementation", "code", "runbook", "invoke"],
        "content": ["def ", "class ", "function", "import ", "implementation", "execute"],
    }

    def __init__(self):
        """Initialize intent classifier."""
        pass

    def classify(
        self,
        file_path: str,
        content_sample: str = "",
        file_type: str = "",
    ) -> IntentResult:
        """
        Classify file intent using rule-based heuristics.

        Args:
            file_path: Path to file
            content_sample: First 500 chars of file
            file_type: File extension

        Returns:
            IntentResult with chunk_type, when_to_load, retrieval_triggers
        """
        path_lower = file_path.lower()
        content_lower = content_sample.lower() if content_sample else ""

        # Determine chunk_type
        chunk_type = self._determine_chunk_type(path_lower, content_lower)

        # Generate when_to_load conditions
        when_to_load = self._generate_conditions(chunk_type, file_path, content_lower)

        # Generate retrieval triggers
        triggers = self._generate_triggers(chunk_type, content_lower)

        return IntentResult(
            chunk_type=chunk_type,
            when_to_load=when_to_load,
            retrieval_triggers=triggers,
        )

    def _determine_chunk_type(self, path: str, content: str) -> str:
        """Determine chunk_type using pattern matching."""

        # Check patterns in order of specificity
        if self._matches_patterns(path, content, self.CONTRACT_PATTERNS):
            return "contract"

        if self._matches_patterns(path, content, self.METHODOLOGY_PATTERNS):
            return "methodology"

        if self._matches_patterns(path, content, self.ARCHITECTURE_PATTERNS):
            return "architecture"

        if self._matches_patterns(path, content, self.EXECUTION_PATTERNS):
            return "execution"

        # Default
        return "reference"

    def _matches_patterns(self, path: str, content: str, patterns: dict) -> bool:
        """Check if path/content matches pattern group."""
        # Check keywords in path
        for keyword in patterns.get("keywords", []):
            if keyword in path:
                return True

        # Check content patterns
        for pattern in patterns.get("content", []):
            if pattern in content:
                return True

        return False

    def _generate_conditions(self, chunk_type: str, file_path: str, content: str) -> list[str]:
        """Generate when_to_load conditions based on type."""

        base_conditions = {
            "contract": [
                f"Agent needs {file_path.split('/')[-1].replace('.', ' ')} rules reference",
                "Validating behavior against system constraints",
                "Enforcing guardrails on agent output",
            ],
            "methodology": [
                f"Agent needs {chunk_type} guidance for task",
                "Implementing best practices or patterns",
                "Refining approach or methodology",
            ],
            "architecture": [
                "Agent needs system design context",
                "Understanding component relationships",
                "Analyzing architectural implications",
            ],
            "execution": [
                "Agent needs implementation details",
                "Writing or debugging code",
                "Understanding workflow execution",
            ],
            "reference": [
                "Agent needs lookup or definition",
                "Cross-referencing related concepts",
                "Validating against baseline",
            ],
        }

        return base_conditions.get(chunk_type, base_conditions["reference"])

    def _generate_triggers(self, chunk_type: str, content: str) -> list[str]:
        """Generate semantic retrieval triggers."""

        triggers = {
            "contract": [
                "guardrails",
                "enforcement rules",
                "system constraints",
                "contract validation",
            ],
            "methodology": [
                "framework reference",
                "best practices",
                "methodology guidance",
                "pattern implementation",
            ],
            "architecture": [
                "system design",
                "component interaction",
                "architectural patterns",
                "dependency mapping",
            ],
            "execution": [
                "implementation details",
                "code execution",
                "workflow steps",
                "runbook procedures",
            ],
            "reference": [
                "definition lookup",
                "concept reference",
                "glossary entry",
                "index reference",
            ],
        }

        return triggers.get(chunk_type, triggers["reference"])
