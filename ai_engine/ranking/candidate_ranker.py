"""Candidate ranking module.

Ranks candidates descending by hybrid_score matching Notebook 06 & 08.
"""

from typing import List, Tuple
from ..models.candidate import MatchingResult, ResumeInformation, CandidateRankingResult


def rank_candidates(
    candidate_pairs: List[Tuple[ResumeInformation, MatchingResult]]
) -> List[CandidateRankingResult]:
    """Sort candidates by hybrid_score descending and assign 1-based ranks.

    Args:
        candidate_pairs: List of (ResumeInformation, MatchingResult) tuples.

    Returns:
        List of CandidateRankingResult sorted by rank (Rank 1 = highest score).
    """
    if not candidate_pairs:
        return []

    # Sort descending by hybrid_score
    sorted_pairs = sorted(
        candidate_pairs, key=lambda pair: pair[1].hybrid_score, reverse=True
    )

    ranked_results: List[CandidateRankingResult] = []
    for rank_idx, (resume_info, matching_result) in enumerate(sorted_pairs, start=1):
        ranked_results.append(
            CandidateRankingResult(
                rank=rank_idx,
                candidate_id=matching_result.candidate_id or resume_info.id,
                hybrid_score=matching_result.hybrid_score,
                matching_result=matching_result,
                resume_info=resume_info,
            )
        )

    return ranked_results
