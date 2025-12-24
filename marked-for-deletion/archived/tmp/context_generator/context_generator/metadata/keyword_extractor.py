"""Extract searchable keywords using multiple strategies."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class KeywordResult:
    """Keyword extraction result."""
    semantic: list[str]
    bm25: list[str]
    entities: list[str]
    topics: list[str]


class KeywordExtractor:
    """Extract searchable keywords using multiple strategies."""

    # Stop words for BM25 (simplified)
    STOP_WORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
        "have", "has", "do", "does", "will", "would", "could", "should", "may",
        "might", "can", "this", "that", "these", "those", "i", "you", "he", "she",
        "it", "we", "they", "what", "which", "who", "when", "where", "why", "how"
    }

    # Topic keywords by common patterns
    TOPIC_PATTERNS = {
        "contract": ["contract", "guardrail", "enforce", "mandate", "rule", "constraint"],
        "framework": ["framework", "pattern", "template", "methodology", "approach"],
        "architecture": ["architect", "design", "component", "system", "interface", "module"],
        "workflow": ["workflow", "process", "step", "orchestrat", "execut", "invoke"],
        "knowledge": ["knowledge", "knowledgebase", "kb", "reference", "document"],
        "configuration": ["config", "env", "setting", "parameter", "option", "flag"],
        "testing": ["test", "validation", "verify", "check", "assert", "unit", "integration"],
    }

    def __init__(self):
        """Initialize keyword extractor."""
        pass

    def extract(
        self,
        content: str,
        file_path: str,
        symbols: list[str] | None = None,
    ) -> KeywordResult:
        """
        Extract keywords using multiple strategies.

        Args:
            content: File content
            file_path: Path to file
            symbols: Extracted symbols (class/function names)

        Returns:
            KeywordResult with semantic, bm25, entities, topics
        """
        return KeywordResult(
            semantic=self._extract_semantic(file_path, content[:500]),
            bm25=self._extract_bm25(content),
            entities=self._extract_entities(symbols or []),
            topics=self._extract_topics(content, file_path),
        )

    def _extract_semantic(self, file_path: str, content_sample: str) -> list[str]:
        """Extract semantic keywords from path and content patterns."""
        keywords = []

        # From filename
        file_name = Path(file_path).stem.lower()
        for part in file_name.replace("-", "_").replace(".", "_").split("_"):
            if part and len(part) > 2:
                keywords.append(part)

        # From content patterns (look for common patterns)
        patterns = [
            r"(?:def|class)\s+(\w+)",  # Function/class names
            r"(?:import|from)\s+(\w+)",  # Imports
            r"# (\w+[\w\s]*)",  # Comments (single word after #)
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content_sample, re.IGNORECASE)
            keywords.extend([m.lower() for m in matches if len(m) > 2])

        # Deduplicate and limit
        return list(dict.fromkeys(keywords))[:5]

    def _extract_bm25(self, content: str) -> list[str]:
        """Extract BM25 terms (TF-IDF style word frequency)."""
        # Tokenize
        words = re.findall(r"\b\w+\b", content.lower())

        # Filter stop words and short words
        filtered = [w for w in words if w not in self.STOP_WORDS and len(w) > 3]

        # Count frequency (simple TF)
        word_freq = {}
        for word in filtered:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

        # Return top unique terms
        return [word for word, _ in sorted_words[:3]]

    def _extract_entities(self, symbols: list[str]) -> list[str]:
        """Extract named entities from symbols (class/function names)."""
        # Take up to 3 most "important" looking symbols (CamelCase usually important)
        entities = []
        for sym in symbols[:10]:
            # Prefer CamelCase (likely classes)
            if any(c.isupper() for c in sym[1:]):
                entities.append(sym.lower())

        return entities[:3]

    def _extract_topics(self, content: str, file_path: str) -> list[str]:
        """Extract topic categories from content and path."""
        content_lower = content.lower()
        path_lower = file_path.lower()
        combined = f"{path_lower} {content_lower[:500]}"

        topics = []
        for topic, keywords in self.TOPIC_PATTERNS.items():
            for keyword in keywords:
                if keyword in combined:
                    topics.append(topic)
                    break

        return list(dict.fromkeys(topics))[:3]
