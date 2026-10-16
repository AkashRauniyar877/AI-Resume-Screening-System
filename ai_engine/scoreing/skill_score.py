"""Skill score calculation module."""

from typing import List
from ..matching.keyword_matcher import calculate_skill_match


def calculate_skill_score(
    candidate_skills: List[str], required_skills: List[str]
) -> float:
    """Calculate skill coverage percentage for candidate against required skills.

    Args:
        candidate_skills: Candidate extracted skills.
        required_skills: Required skills from job description.

    Returns:
        Skill coverage percentage float (0.0..100.0).
    """
    _, _, coverage = calculate_skill_match(candidate_skills, required_skills)
    return coverage
