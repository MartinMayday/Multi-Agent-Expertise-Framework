"""Search metadata and RAGAS preparation for retrieval evaluation."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RAGASMetrics:
    """RAGAS (Retrieval-Augmented Generation Assessment) metrics."""
    relevance_score: float = 0.0  # 0.0-1.0 (higher = more relevant)
    coherence_score: float = 0.0   # 0.0-1.0 (higher = more coherent)
    faithfulness_score: float = 0.0  # 0.0-1.0 (higher = more faithful)
    answer_relevance: float = 0.0   # 0.0-1.0 (higher = better answers)


@dataclass
class SearchMetadata:
    """Complete metadata for search and retrieval."""
    file_id: str
    file_path: str
    file_name: str
    
    # Basic metadata
    tokens: int
    chunk_type: str
    keywords: list[str] = field(default_factory=list)
    priority: str = "medium"  # high, medium, low
    
    # Search hints
    bm25_terms: list[str] = field(default_factory=list)
    semantic_signals: list[str] = field(default_factory=list)
    
    # Retrieval conditions
    when_to_load: list[str] = field(default_factory=list)
    retrieval_triggers: list[str] = field(default_factory=list)
    
    # RAGAS metrics (computed)
    ragas_metrics: Optional[RAGASMetrics] = None
    
    # Ranking signals
    retrieval_score: float = 0.0  # Combined ranking score
    confidence: float = 0.0  # Confidence in ranking


class RAGASPreparator:
    """Prepare files for RAGAS evaluation metrics."""
    
    @staticmethod
    def prepare_file(
        file_id: str,
        file_path: str,
        file_name: str,
        tokens: int,
        chunk_type: str,
        keywords: list[str],
        summary: str = "",
        when_to_load: list[str] | None = None,
        retrieval_triggers: list[str] | None = None,
    ) -> SearchMetadata:
        """
        Prepare file metadata for RAGAS evaluation.
        
        Args:
            file_id: File identifier
            file_path: Relative file path
            file_name: File name
            tokens: Token count
            chunk_type: Classification
            keywords: File keywords
            summary: File summary
            when_to_load: Loading conditions
            retrieval_triggers: Semantic triggers
            
        Returns:
            SearchMetadata with RAGAS preparation
        """
        # Determine priority
        priority = RAGASPreparator._determine_priority(tokens, len(when_to_load or []))
        
        # Extract BM25 terms (distinctive keywords)
        bm25_terms = RAGASPreparator._extract_bm25_terms(keywords)
        
        # Generate semantic signals
        semantic_signals = RAGASPreparator._generate_semantic_signals(
            chunk_type, keywords, summary
        )
        
        # Compute RAGAS metrics
        ragas = RAGASPreparator._compute_ragas_metrics(
            chunk_type=chunk_type,
            keywords=keywords,
            summary=summary,
            tokens=tokens,
            when_to_load=when_to_load or []
        )
        
        return SearchMetadata(
            file_id=file_id,
            file_path=file_path,
            file_name=file_name,
            tokens=tokens,
            chunk_type=chunk_type,
            keywords=keywords,
            priority=priority,
            bm25_terms=bm25_terms,
            semantic_signals=semantic_signals,
            when_to_load=when_to_load or [],
            retrieval_triggers=retrieval_triggers or [],
            ragas_metrics=ragas,
        )
    
    @staticmethod
    def _determine_priority(tokens: int, condition_count: int) -> str:
        """
        Determine priority level based on size and importance.
        
        Args:
            tokens: Token count
            condition_count: Number of when_to_load conditions
            
        Returns:
            Priority level: high, medium, low
        """
        # High priority: large files with many conditions
        if tokens > 2000 or condition_count >= 3:
            return "high"
        
        # Low priority: small, simple files
        if tokens < 300 and condition_count == 0:
            return "low"
        
        # Medium by default
        return "medium"
    
    @staticmethod
    def _extract_bm25_terms(keywords: list[str]) -> list[str]:
        """
        Extract BM25 terms (most distinctive keywords).
        
        Args:
            keywords: All keywords
            
        Returns:
            Top 3-5 most distinctive terms
        """
        # Return longer, more distinctive keywords (length > 4)
        distinctive = [kw for kw in keywords if len(kw) > 4]
        
        # If not enough distinctive terms, include all
        if len(distinctive) < 3:
            distinctive = keywords
        
        # Return top by length (longer = more specific)
        return sorted(distinctive, key=len, reverse=True)[:5]
    
    @staticmethod
    def _generate_semantic_signals(
        chunk_type: str,
        keywords: list[str],
        summary: str = ""
    ) -> list[str]:
        """
        Generate semantic signals for similarity matching.
        
        Args:
            chunk_type: File classification
            keywords: Keywords
            summary: File summary
            
        Returns:
            Semantic signal phrases
        """
        signals = []
        
        # Add chunk type as signal
        if chunk_type:
            signals.append(f"{chunk_type} file")
        
        # Add top keywords as signals
        for kw in keywords[:3]:
            signals.append(kw)
        
        # Extract noun phrases from summary
        if summary:
            # Simple heuristic: capitalize words in summary as potential concepts
            words = summary.split()
            for word in words:
                if word and word[0].isupper() and len(word) > 5:
                    signals.append(word.lower())
        
        # Remove duplicates and return
        return list(dict.fromkeys(signals))[:5]
    
    @staticmethod
    def _compute_ragas_metrics(
        chunk_type: str,
        keywords: list[str],
        summary: str = "",
        tokens: int = 0,
        when_to_load: list[str] | None = None,
    ) -> RAGASMetrics:
        """
        Compute RAGAS metrics for file quality assessment.
        
        RAGAS evaluates:
        - Relevance: How relevant is the file to typical queries
        - Coherence: How well-structured is the content
        - Faithfulness: How accurate/reliable is the content
        - Answer Relevance: How likely to produce good answers
        
        Args:
            chunk_type: File classification
            keywords: Keywords (indicate content clarity)
            summary: File summary (indicate coherence)
            tokens: File size (indicate completeness)
            when_to_load: Conditions (indicate clarity of purpose)
            
        Returns:
            RAGASMetrics with computed scores
        """
        metrics = RAGASMetrics()
        
        # Relevance: Based on keyword count and chunk type clarity
        # More keywords = clearer content = higher relevance
        relevance = min(1.0, len(keywords) / 10.0)  # 10 keywords = max
        
        # Boost for certain chunk types (more likely to be relevant)
        if chunk_type.lower() in ['contract', 'methodology', 'architecture']:
            relevance = min(1.0, relevance + 0.2)
        
        metrics.relevance_score = relevance
        
        # Coherence: Based on summary and structure
        # Non-empty summary = better coherence
        coherence = 0.7 if summary else 0.5
        
        # Boost for larger files (more comprehensive = more coherent)
        if tokens > 1000:
            coherence = min(1.0, coherence + 0.15)
        
        metrics.coherence_score = coherence
        
        # Faithfulness: Based on explicit when_to_load conditions
        # Clear conditions = trustworthy source
        conditions = when_to_load or []
        faithfulness = min(1.0, len(conditions) / 3.0)  # 3 conditions = max
        
        # Boost for structured types
        if chunk_type.lower() in ['contract', 'architecture']:
            faithfulness = min(1.0, faithfulness + 0.25)
        
        metrics.faithfulness_score = faithfulness
        
        # Answer Relevance: Combined score
        # How likely this file will produce good answers
        answer_relevance = (
            0.3 * metrics.relevance_score +
            0.3 * metrics.coherence_score +
            0.4 * metrics.faithfulness_score
        )
        
        metrics.answer_relevance = answer_relevance
        
        return metrics


class SearchMetadataBuilder:
    """Build complete search metadata for all files."""
    
    def __init__(self):
        """Initialize metadata builder."""
        self.ragas_prep = RAGASPreparator()
    
    def build_metadata(
        self,
        file_id: str,
        file_path: str,
        file_name: str,
        tokens: int,
        chunk_type: str,
        keywords: list[str],
        priority: str = "medium",
        summary: str = "",
        when_to_load: list[str] | None = None,
        retrieval_triggers: list[str] | None = None,
    ) -> SearchMetadata:
        """
        Build complete search metadata for a file.
        
        Args:
            file_id: File identifier
            file_path: Relative file path
            file_name: File name
            tokens: Token count
            chunk_type: Classification
            keywords: File keywords
            priority: Priority level
            summary: File summary/description
            when_to_load: Loading conditions
            retrieval_triggers: Semantic triggers
            
        Returns:
            Complete SearchMetadata
        """
        return self.ragas_prep.prepare_file(
            file_id=file_id,
            file_path=file_path,
            file_name=file_name,
            tokens=tokens,
            chunk_type=chunk_type,
            keywords=keywords,
            summary=summary,
            when_to_load=when_to_load,
            retrieval_triggers=retrieval_triggers,
        )
    
    def build_collection(self, files: list[dict]) -> list[SearchMetadata]:
        """
        Build search metadata for collection of files.
        
        Args:
            files: List of file dicts with metadata
            
        Returns:
            List of SearchMetadata objects
        """
        metadata_list = []
        
        for file in files:
            metadata = self.build_metadata(
                file_id=file.get('id', 'unknown'),
                file_path=file.get('path', ''),
                file_name=file.get('name', ''),
                tokens=file.get('tokens', 0),
                chunk_type=file.get('chunk_type', 'reference'),
                keywords=file.get('keywords', []),
                priority=file.get('priority', 'medium'),
                summary=file.get('summary', ''),
                when_to_load=file.get('when_to_load'),
                retrieval_triggers=file.get('retrieval_triggers'),
            )
            metadata_list.append(metadata)
        
        return metadata_list
    
    def compute_collection_stats(
        self, metadata_list: list[SearchMetadata]
    ) -> dict:
        """
        Compute aggregate statistics for collection.
        
        Args:
            metadata_list: List of SearchMetadata objects
            
        Returns:
            Statistics dict
        """
        if not metadata_list:
            return {}
        
        # Aggregate RAGAS scores
        avg_relevance = sum(
            m.ragas_metrics.relevance_score 
            for m in metadata_list if m.ragas_metrics
        ) / len(metadata_list)
        
        avg_coherence = sum(
            m.ragas_metrics.coherence_score 
            for m in metadata_list if m.ragas_metrics
        ) / len(metadata_list)
        
        avg_faithfulness = sum(
            m.ragas_metrics.faithfulness_score 
            for m in metadata_list if m.ragas_metrics
        ) / len(metadata_list)
        
        avg_answer_relevance = sum(
            m.ragas_metrics.answer_relevance 
            for m in metadata_list if m.ragas_metrics
        ) / len(metadata_list)
        
        return {
            "total_files": len(metadata_list),
            "avg_tokens": sum(m.tokens for m in metadata_list) / len(metadata_list),
            "avg_keywords": sum(len(m.keywords) for m in metadata_list) / len(metadata_list),
            "chunk_type_distribution": self._count_by_chunk_type(metadata_list),
            "priority_distribution": self._count_by_priority(metadata_list),
            "ragas": {
                "avg_relevance": avg_relevance,
                "avg_coherence": avg_coherence,
                "avg_faithfulness": avg_faithfulness,
                "avg_answer_relevance": avg_answer_relevance,
            }
        }
    
    @staticmethod
    def _count_by_chunk_type(metadata_list: list[SearchMetadata]) -> dict:
        """Count files by chunk type."""
        counts = {}
        for m in metadata_list:
            chunk_type = m.chunk_type or 'unknown'
            counts[chunk_type] = counts.get(chunk_type, 0) + 1
        return counts
    
    @staticmethod
    def _count_by_priority(metadata_list: list[SearchMetadata]) -> dict:
        """Count files by priority."""
        counts = {}
        for m in metadata_list:
            counts[m.priority] = counts.get(m.priority, 0) + 1
        return counts
