"""Pydantic schemas for FastAPI resume screening endpoints."""

from typing import List, Optional, Any
from pydantic import BaseModel, Field


class CandidateInfoSchema(BaseModel):
    """Extracted candidate contact and resume details."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: List[str] = Field(default_factory=list)
    experience_years: float = 0.0


class JobAnalysisSchema(BaseModel):
    """Extracted job description requirements."""
    required_skills: List[str] = Field(default_factory=list)
    required_experience: float = 0.0
    required_education: List[str] = Field(default_factory=list)


class ParseResumeResponse(BaseModel):
    """Response schema for single resume parsing."""
    filename: str
    extracted_text: str
    candidate_info: CandidateInfoSchema


class SingleMatchResultSchema(BaseModel):
    """Match metrics for a single resume against a job description."""
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    skill_coverage: float = 0.0
    tfidf_score: float = 0.0
    tfidf_normalized: float = 0.0
    semantic_score: float = 0.0
    semantic_normalized: float = 0.0
    experience_years: float = 0.0
    experience_score: float = 0.0
    hybrid_score: float = 0.0


class ScreenResumeResponse(BaseModel):
    """Response schema for single candidate screening."""
    filename: str
    resume_id: Optional[str] = None
    resume_actions: Optional[dict] = None
    candidate_info: CandidateInfoSchema
    match_results: SingleMatchResultSchema


class RankedCandidateSchema(BaseModel):
    """Schema for a single candidate within batch ranking response."""
    rank: int
    candidate_id: Optional[Any] = None
    resume_id: Optional[str] = None
    filename: str
    hybrid_score: float
    candidate_info: CandidateInfoSchema
    match_results: SingleMatchResultSchema
    resume_actions: Optional[dict] = None


class BatchScreenResponse(BaseModel):
    """Response schema for batch candidate screening and ranking."""
    total_candidates: int
    job_description_analysis: JobAnalysisSchema
    ranked_candidates: List[RankedCandidateSchema]
