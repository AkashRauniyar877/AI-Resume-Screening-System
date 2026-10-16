"""Experience score calculation module.

Implements experience ratio scoring matching Notebook 05.
"""


def calculate_experience_score(
    candidate_experience: float, required_experience: float
) -> float:
    """Calculate experience score as a percentage of required experience capped at 100%.

    Matches Notebook 05 logic.

    Args:
        candidate_experience: Extracted candidate experience in years.
        required_experience: Required experience in years from job description.

    Returns:
        Experience score float between 0.0 and 100.0.
    """
    if required_experience <= 0:
        return 0.0

    score = (candidate_experience / required_experience) * 100.0
    return min(score, 100.0)
