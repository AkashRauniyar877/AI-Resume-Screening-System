"""Data structures and models for AI Resume Screening System.

Defines structured data representations for resumes, job descriptions,
matching results, and candidate rankings.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ResumeInformation:
    """Extracted information from a resume."""
    raw_text: str = ""
    cleaned_text: str = ""
    processed_text: str = ""
    id: Optional[Any] = None
    category: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    education: List[str] = field(default_factory=list)
    experience_years: float = 0.0


@dataclass
class JobDescriptionInformation:
    """Extracted requirements from a job description."""
    raw_text: str = ""
    cleaned_text: str = ""
    processed_text: str = ""
    required_skills: List[str] = field(default_factory=list)
    required_experience: float = 0.0
    required_education: List[str] = field(default_factory=list)


@dataclass
class MatchingResult:
    """Calculated matching scores and skill analysis for a candidate."""
    candidate_id: Optional[Any] = None
    category: Optional[str] = None
    tfidf_score: float = 0.0
    tfidf_normalized: float = 0.0
    semantic_score: float = 0.0
    semantic_normalized: float = 0.0
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    skill_coverage: float = 0.0
    experience_years: float = 0.0
    experience_score: float = 0.0
    hybrid_score: float = 0.0


@dataclass
class CandidateRankingResult:
    """Final ranked candidate result."""
    rank: int
    candidate_id: Optional[Any]
    hybrid_score: float
    matching_result: MatchingResult
    resume_info: ResumeInformation
