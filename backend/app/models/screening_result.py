"""MongoDB Screening Result Document model helper."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def create_screening_result_document(
    job_id: str,
    candidate_id: str,
    resume_id: str,
    matched_skills: List[str],
    missing_skills: List[str],
    skill_coverage: float,
    tfidf_score: float,
    tfidf_normalized: float,
    semantic_score: float,
    semantic_normalized: float,
    experience_score: float,
    hybrid_score: float,
    rank: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    education: Optional[List[str]] = None,
    experience_years: Optional[float] = 0.0,
    skills: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a MongoDB document dictionary for a Screening Result.

    All scores come directly from the ai_engine.

    Returns:
        Dictionary document ready for MongoDB insertion.
    """
    return {
        "job_id": job_id,
        "candidate_id": candidate_id,
        "resume_id": resume_id,
        "name": name,
        "email": email,
        "phone": phone,
        "education": education or [],
        "experience_years": float(experience_years or 0.0),
        "skills": skills or [],
        "matched_skills": matched_skills or [],
        "missing_skills": missing_skills or [],
        "skill_coverage": float(skill_coverage),
        "tfidf_score": float(tfidf_score),
        "tfidf_normalized": float(tfidf_normalized),
        "semantic_score": float(semantic_score),
        "semantic_normalized": float(semantic_normalized),
        "experience_score": float(experience_score),
        "hybrid_score": float(hybrid_score),
        "rank": int(rank),
        "screening_date": datetime.now(timezone.utc),
    }
