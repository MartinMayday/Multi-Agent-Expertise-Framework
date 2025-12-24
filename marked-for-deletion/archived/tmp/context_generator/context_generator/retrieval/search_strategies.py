"""Hybrid search strategies with RRF, BM25, and semantic ranking."""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RankedFile:
    """File with computed ranking scores."""
    file_id: str
    file_path: str
    file_name: str
    tokens: int
    chunk_type: str
    keywords: list[str] = field(default_factory=list)
    
    bm25_score: float = 0.0
    semantic_score: float = 0.0
    keyword_match_score: float = 0.0
    priority_boost: float = 1.0
    
    combined_score: float = 0.0
    rrf_rank: int = 0


@dataclass
class RankingWeights:
    """Weights for hybrid ranking combination."""
    bm25: float = 0.3
    semantic: float = 0.4
    keywords: float = 0.2
    priority: float = 0.1
    
    def normalize(self):
        """Ensure weights sum to 1.0."""
        total = self.bm25 + self.semantic + self.keywords + self.priority
        if total > 0:
            self.bm25 /= total
            self.semantic /= total
            self.keywords /= total
            self.priority /= total


class BM25Scorer:
    """BM25 ranking algorithm (simplified TF-IDF variant)."""
    
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        """
        Initialize BM25 scorer.
        
        Args:
            k1: Term frequency saturation point (default: 1.5)
            b: Document length normalization (default: 0.75)
        """
        self.k1 = k1
        self.b = b
        self.avg_doc_length = 0.0
        self.doc_count = 0
        self.idf_cache = {}
    
    def add_documents(self, documents: list[dict]):
        """
        Compute IDF values from document collection.
        
        Args:
            documents: List of dicts with 'keywords' and 'tokens' keys
        """
        self.doc_count = len(documents)
        if self.doc_count == 0:
            return
        
        # Compute average document length
        self.avg_doc_length = sum(d.get('tokens', 0) for d in documents) / self.doc_count
        
        # Compute IDF for each term
        term_counts = {}
        for doc in documents:
            keywords = set(doc.get('keywords', []))
            for keyword in keywords:
                term_counts[keyword] = term_counts.get(keyword, 0) + 1
        
        # IDF = log((N - n + 0.5) / (n + 0.5))
        for term, count in term_counts.items():
            idf = math.log((self.doc_count - count + 0.5) / (count + 0.5) + 1.0)
            self.idf_cache[term] = idf
    
    def score_document(self, keywords: list[str], tokens: int) -> float:
        """
        Compute BM25 score for a document.
        
        Args:
            keywords: Document keywords/terms
            tokens: Document length in tokens
            
        Returns:
            BM25 score (0.0+)
        """
        if self.doc_count == 0 or self.avg_doc_length == 0:
            return 0.0
        
        score = 0.0
        keyword_counts = {}
        
        # Count keyword occurrences
        for kw in keywords:
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        
        # BM25 formula: Σ IDF(qi) * (tf(qi, D) * (k1 + 1)) / (tf(qi, D) + k1 * (1 - b + b * |D| / avgdl))
        for keyword, freq in keyword_counts.items():
            idf = self.idf_cache.get(keyword, 0.0)
            
            # Normalize term frequency by document length
            norm_length = 1.0 - self.b + self.b * (tokens / max(self.avg_doc_length, 1.0))
            tf_component = (freq * (self.k1 + 1)) / (freq + self.k1 * norm_length)
            
            score += idf * tf_component
        
        return max(0.0, score)


class SemanticScorer:
    """Semantic similarity scoring using keyword overlap."""
    
    @staticmethod
    def score_similarity(query_keywords: list[str], doc_keywords: list[str]) -> float:
        """
        Compute similarity between two keyword sets.
        
        Uses Jaccard similarity: intersection / union
        
        Args:
            query_keywords: Query keywords/terms
            doc_keywords: Document keywords
            
        Returns:
            Similarity score (0.0-1.0)
        """
        if not query_keywords or not doc_keywords:
            return 0.0
        
        query_set = set(k.lower() for k in query_keywords)
        doc_set = set(k.lower() for k in doc_keywords)
        
        intersection = len(query_set & doc_set)
        union = len(query_set | doc_set)
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def score_keyword_match(query: str, keywords: list[str], chunk_type: str = "") -> float:
        """
        Score how well keywords match a query.
        
        Args:
            query: Search query or intent
            keywords: File keywords
            chunk_type: File chunk type (for bonus matching)
            
        Returns:
            Match score (0.0-1.0)
        """
        query_lower = query.lower()
        
        # Exact keyword matches
        exact_matches = sum(1 for kw in keywords if kw.lower() == query_lower)
        
        # Partial matches
        partial_matches = sum(
            0.5 for kw in keywords 
            if query_lower in kw.lower() or kw.lower() in query_lower
        )
        
        # Chunk type bonus
        chunk_bonus = 0.2 if chunk_type.lower() in query_lower else 0.0
        
        # Normalize to 0-1
        score = min(1.0, (exact_matches + partial_matches + chunk_bonus) / max(len(keywords), 1))
        
        return score


class RFRanker:
    """Reciprocal Rank Fusion (RRF) combiner."""
    
    @staticmethod
    def combine_ranks(
        ranked_files: list[RankedFile],
        weights: RankingWeights,
    ) -> list[RankedFile]:
        """
        Combine multiple ranking signals using RRF.
        
        RRF formula: score = Σ (weight_i / (60 + rank_i))
        
        Args:
            ranked_files: Files with individual scores
            weights: Weights for each ranking signal
            
        Returns:
            Ranked files with combined scores (sorted by combined_score desc)
        """
        weights.normalize()
        
        # Assign ranks within each scoring method
        bm25_sorted = sorted(
            enumerate(ranked_files),
            key=lambda x: x[1].bm25_score,
            reverse=True
        )
        semantic_sorted = sorted(
            enumerate(ranked_files),
            key=lambda x: x[1].semantic_score,
            reverse=True
        )
        keyword_sorted = sorted(
            enumerate(ranked_files),
            key=lambda x: x[1].keyword_match_score,
            reverse=True
        )
        priority_sorted = sorted(
            enumerate(ranked_files),
            key=lambda x: x[1].priority_boost,
            reverse=True
        )
        
        # Create rank maps
        bm25_ranks = {idx: rank + 1 for rank, (idx, _) in enumerate(bm25_sorted)}
        semantic_ranks = {idx: rank + 1 for rank, (idx, _) in enumerate(semantic_sorted)}
        keyword_ranks = {idx: rank + 1 for rank, (idx, _) in enumerate(keyword_sorted)}
        priority_ranks = {idx: rank + 1 for rank, (idx, _) in enumerate(priority_sorted)}
        
        # Compute RRF scores
        for idx, file in enumerate(ranked_files):
            rrf_score = (
                weights.bm25 / (60 + bm25_ranks.get(idx, 60)) +
                weights.semantic / (60 + semantic_ranks.get(idx, 60)) +
                weights.keywords / (60 + keyword_ranks.get(idx, 60)) +
                weights.priority / (60 + priority_ranks.get(idx, 60))
            )
            
            file.combined_score = rrf_score
            file.rrf_rank = bm25_ranks.get(idx, 0)
        
        # Sort by combined score
        return sorted(ranked_files, key=lambda f: f.combined_score, reverse=True)


class HybridSearchStrategy:
    """Complete hybrid search ranking combining BM25, semantic, and keyword signals."""
    
    def __init__(self, weights: Optional[RankingWeights] = None):
        """
        Initialize hybrid search strategy.
        
        Args:
            weights: Custom ranking weights (default: balanced)
        """
        self.bm25_scorer = BM25Scorer()
        self.semantic_scorer = SemanticScorer()
        self.weights = weights or RankingWeights()
        self.weights.normalize()
    
    def prepare_documents(self, files: list[dict]) -> None:
        """
        Prepare document collection for BM25 scoring.
        
        Args:
            files: List of file dicts with 'keywords' and 'tokens'
        """
        self.bm25_scorer.add_documents(files)
    
    def rank_files(
        self,
        query: str,
        query_keywords: list[str],
        files: list[dict],
    ) -> list[RankedFile]:
        """
        Rank files against a query using hybrid strategies.
        
        Args:
            query: Search query/intent text
            query_keywords: Query keywords/terms
            files: List of file dicts with metadata
            
        Returns:
            Ranked files sorted by combined score (highest first)
        """
        # Prepare BM25 scorer with collection
        self.bm25_scorer.add_documents(files)
        
        ranked_files = []
        
        for file in files:
            file_id = file.get('id', 'unknown')
            file_path = file.get('path', '')
            file_name = file.get('name', '')
            tokens = file.get('tokens', 0)
            chunk_type = file.get('chunk_type', '')
            keywords = file.get('keywords', [])
            
            # Compute BM25 score
            bm25_score = self.bm25_scorer.score_document(keywords, tokens)
            
            # Compute semantic similarity
            semantic_score = self.semantic_scorer.score_similarity(query_keywords, keywords)
            
            # Compute keyword match score
            keyword_match_score = self.semantic_scorer.score_keyword_match(
                query, keywords, chunk_type
            )
            
            # Priority boost based on chunk type and token count
            priority_boost = self._compute_priority_boost(chunk_type, tokens)
            
            ranked_files.append(RankedFile(
                file_id=file_id,
                file_path=file_path,
                file_name=file_name,
                tokens=tokens,
                chunk_type=chunk_type,
                keywords=keywords,
                bm25_score=bm25_score,
                semantic_score=semantic_score,
                keyword_match_score=keyword_match_score,
                priority_boost=priority_boost,
            ))
        
        # Combine rankings using RRF
        return RFRanker.combine_ranks(ranked_files, self.weights)
    
    def _compute_priority_boost(self, chunk_type: str, tokens: int) -> float:
        """
        Compute priority boost based on chunk type and size.
        
        Args:
            chunk_type: File classification
            tokens: Document token count
            
        Returns:
            Boost factor (0.5-2.0)
        """
        # Base boost by chunk type
        type_boost = {
            'contract': 1.5,      # Contracts are high priority
            'architecture': 1.3,  # Architecture important for context
            'methodology': 1.2,   # Methodology useful for guidance
            'execution': 1.0,     # Implementation details baseline
            'reference': 0.8,     # References lower priority
        }
        
        boost = type_boost.get(chunk_type.lower(), 1.0)
        
        # Additional boost for larger documents (more comprehensive)
        if tokens > 2000:
            boost *= 1.2
        elif tokens < 500:
            boost *= 0.9
        
        return min(2.0, max(0.5, boost))
    
    def rank_by_intent(
        self,
        intent: str,
        files: list[dict],
        chunk_type_filter: Optional[list[str]] = None,
    ) -> list[RankedFile]:
        """
        Rank files by matching agent intent to when_to_load conditions.
        
        Args:
            intent: Agent's stated intent/task
            files: File metadata list
            chunk_type_filter: Optional list of chunk types to include
            
        Returns:
            Ranked files filtered and sorted by relevance to intent
        """
        # Filter by chunk type if specified
        if chunk_type_filter:
            filtered_files = [
                f for f in files
                if f.get('chunk_type', '').lower() in [ct.lower() for ct in chunk_type_filter]
            ]
        else:
            filtered_files = files
        
        if not filtered_files:
            return []
        
        # Extract keywords from intent
        intent_keywords = self._extract_intent_keywords(intent)
        
        # Rank using hybrid strategy
        ranked = self.rank_files(intent, intent_keywords, filtered_files)
        
        return ranked
    
    def rank_by_trigger(
        self,
        trigger_phrase: str,
        files: list[dict],
    ) -> list[RankedFile]:
        """
        Rank files by matching a retrieval trigger phrase.
        
        Args:
            trigger_phrase: Semantic trigger phrase
            files: File metadata list
            
        Returns:
            Ranked files matching trigger
        """
        # Extract keywords from trigger
        trigger_keywords = self._extract_intent_keywords(trigger_phrase)
        
        # Rank files
        ranked = self.rank_files(trigger_phrase, trigger_keywords, files)
        
        # Filter to files with meaningful scores
        return [f for f in ranked if f.combined_score > 0.1]
    
    @staticmethod
    def _extract_intent_keywords(text: str) -> list[str]:
        """
        Extract keywords from intent or trigger text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction: split by spaces, filter short words
        words = text.lower().split()
        keywords = [w for w in words if len(w) > 3 and w.isalpha()]
        return keywords
