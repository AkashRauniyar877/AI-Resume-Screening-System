"""MongoDB Job Document model helper."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def create_job_document(
    job_title: str,
    job_description: str,
    required_skills: Optional[List[str]] = None,
    required_experience: float = 0.0,
    required_education: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a MongoDB document dictionary for a Job.

    Args:
        job_title: Title of job posting.
        job_description: Raw job description text.
        required_skills: List of required skills from AI engine.
        required_experience: Required experience years from AI engine.
        required_education: Required education degrees from AI engine.

    Returns:
        Dictionary document ready for MongoDB insertion.
    """
    return {
        "job_title": job_title.strip() if job_title else "Job Position",
        "job_description": job_description.strip(),
        "required_skills": required_skills or [],
        "required_experience": float(required_experience),
        "required_education": required_education or [],
        "created_at": datetime.now(timezone.utc),
    }
