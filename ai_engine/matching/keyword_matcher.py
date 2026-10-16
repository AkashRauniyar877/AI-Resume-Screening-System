"""Keyword and skill matching module.

Implements skill overlap, missing skills, and coverage percentage matching Notebook 04.
"""

from typing import List, Set, Tuple


def calculate_skill_match(
    candidate_skills: List[str], required_skills: List[str]
) -> Tuple[List[str], List[str], float]:
    """Calculate matched skills, missing skills, and skill coverage percentage.

    Matches Notebook 04 calculate_skill_match function logic.

    Args:
        candidate_skills: List of skills extracted from candidate resume.
        required_skills: List of skills required by job description.

    Returns:
        Tuple of (matched_skills, missing_skills, skill_coverage_percentage).
    """
    cand_set: Set[str] = set(s.lower() for s in candidate_skills)
    req_set: Set[str] = set(s.lower() for s in required_skills)

    matched = list(cand_set & req_set)
    missing = list(req_set - cand_set)

    if len(req_set) > 0:
        coverage = (len(matched) / len(req_set)) * 100.0
    else:
        coverage = 0.0

    return matched, missing, coverage
