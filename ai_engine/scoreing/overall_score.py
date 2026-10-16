"""Overall hybrid scoring module.

Implements min-max score normalization and weighted hybrid scoring matching Notebook 08.
"""

from typing import Dict, List, Optional
import numpy as np
from ..config.ai_config import DEFAULT_SCORING_WEIGHTS
from ..models.candidate import MatchingResult


def min_max_normalize(scores: np.ndarray) -> np.ndarray:
    """Perform min-max normalization converting scores to 0..100 range.

    Matches Notebook 08 min_max_normalize helper.

    Args:
        scores: Array of raw scores.

    Returns:
        Array of normalized scores.
    """
    if len(scores) == 0:
        return np.array([])

    min_val = np.min(scores)
    max_val = np.max(scores)

    if max_val == min_val:
        # Avoid division by zero if all scores are identical
        return np.zeros_like(scores, dtype=float) if min_val <= 0 else np.full_like(scores, min_val, dtype=float)

    return (scores - min_val) / (max_val - min_val) * 100.0


def calculate_hybrid_score(
    skill_coverage: float,
    semantic_normalized: float,
    tfidf_normalized: float,
    experience_score: float,
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """Calculate hybrid score using weighted component scores.

    Formula from Notebook 08:
    0.35 * skill_coverage + 0.30 * semantic_norm + 0.20 * tfidf_norm + 0.15 * exp_score

    Args:
        skill_coverage: Skill coverage percentage (0..100).
        semantic_normalized: Min-max normalized semantic score (0..100).
        tfidf_normalized: Min-max normalized TF-IDF score (0..100).
        experience_score: Experience score percentage (0..100).
        weights: Optional dictionary of weights (defaults to DEFAULT_SCORING_WEIGHTS).

    Returns:
        Hybrid score float between 0.0 and 100.0.
    """
    if weights is None:
        weights = DEFAULT_SCORING_WEIGHTS

    w_skill = weights.get("skill", 0.35)
    w_semantic = weights.get("semantic", 0.30)
    w_tfidf = weights.get("tfidf", 0.20)
    w_exp = weights.get("experience", 0.15)

    hybrid = (
        w_skill * skill_coverage
        + w_semantic * semantic_normalized
        + w_tfidf * tfidf_normalized
        + w_exp * experience_score
    )
    return float(hybrid)


def compute_batch_hybrid_scores(
    matching_results: List[MatchingResult],
    weights: Optional[Dict[str, float]] = None,
) -> List[MatchingResult]:
    """Compute normalized scores and final hybrid scores across a batch of candidates.

    Args:
        matching_results: List of MatchingResult objects with raw scores filled.
        weights: Optional scoring weights.

    Returns:
        List of MatchingResult objects updated with normalized scores and hybrid_score.
    """
    if not matching_results:
        return []

    tfidf_raw = np.array([m.tfidf_score for m in matching_results])
    semantic_raw = np.array([m.semantic_score for m in matching_results])

    if len(matching_results) > 1:
        tfidf_norm = min_max_normalize(tfidf_raw)
        semantic_norm = min_max_normalize(semantic_raw)
    else:
        # Single candidate fallback: pass raw scores (already 0..100 scale)
        tfidf_norm = np.clip(tfidf_raw, 0, 100)
        semantic_norm = np.clip(semantic_raw, 0, 100)

    for i, res in enumerate(matching_results):
        res.tfidf_normalized = float(tfidf_norm[i])
        res.semantic_normalized = float(semantic_norm[i])
        res.hybrid_score = calculate_hybrid_score(
            skill_coverage=res.skill_coverage,
            semantic_normalized=res.semantic_normalized,
            tfidf_normalized=res.tfidf_normalized,
            experience_score=res.experience_score,
            weights=weights,
        )

    return matching_results
