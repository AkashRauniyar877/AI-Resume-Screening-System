"""Education match score calculation module."""

from typing import List


def calculate_education_score(
    candidate_education: List[str], required_education: List[str]
) -> float:
    """Calculate education match percentage between candidate education and requirements.

    Args:
        candidate_education: List of candidate degrees.
        required_education: List of required degrees.

    Returns:
        Score percentage float (0.0 or 100.0 if any requirement matched, or proportion matched).
    """
    if not required_education:
        return 100.0
    if not candidate_education:
        return 0.0

    cand_set = set(e.lower() for e in candidate_education)
    req_set = set(e.lower() for e in required_education)

    matched = cand_set & req_set
    if matched:
        return 100.0

    return 0.0
