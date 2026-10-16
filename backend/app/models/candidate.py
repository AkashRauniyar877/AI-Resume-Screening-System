"""MongoDB Candidate Document model helper."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def create_candidate_document(
    candidate_id: str,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    skills: Optional[List[str]] = None,
    education: Optional[List[str]] = None,
    experience_years: float = 0.0,
) -> Dict[str, Any]:
    """Build a MongoDB document dictionary for a Candidate.

    Args:
        candidate_id: Unique candidate identifier.
        name: Extracted candidate name (or None).
        email: Extracted candidate email (or None).
        phone: Extracted candidate phone (or None).
        skills: List of extracted skills.
        education: List of extracted degrees.
        experience_years: Extracted experience years.

    Returns:
        Dictionary document ready for MongoDB insertion.
    """
    return {
        "candidate_id": candidate_id,
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills or [],
        "education": education or [],
        "experience_years": float(experience_years),
        "created_at": datetime.now(timezone.utc),
    }
