"""Main orchestration pipeline for AI Resume Screening System.

Parses resumes, extracts information, computes TF-IDF and semantic similarity,
performs skill and experience matching, calculates hybrid scores, and ranks candidates.
"""

from typing import Any, Dict, List, Optional, Union
from .parser import extract_text
from .preprocessing import clean_raw_text, preprocess_text
from .extraction import (
    extract_email,
    extract_phone,
    extract_name,
    extract_skills,
    extract_education,
    extract_experience,
)
from .matching import (
    calculate_skill_match,
    compute_tfidf_similarity,
    compute_semantic_similarity,
)
from .scoreing import calculate_experience_score, compute_batch_hybrid_scores
from .ranking import rank_candidates
from .models import (
    ResumeInformation,
    JobDescriptionInformation,
    MatchingResult,
    CandidateRankingResult,
)


def analyze_job_description(job_description_text: str) -> JobDescriptionInformation:
    """Analyze job description text and extract required skills, experience, and education.

    Matches Notebook 10.

    Args:
        job_description_text: Raw job description text string.

    Returns:
        JobDescriptionInformation dataclass containing requirements.
    """
    cleaned = clean_raw_text(job_description_text)
    processed = preprocess_text(job_description_text)

    req_skills = extract_skills(job_description_text)
    req_exp = extract_experience(job_description_text)
    req_edu = extract_education(job_description_text)

    return JobDescriptionInformation(
        raw_text=job_description_text,
        cleaned_text=cleaned,
        processed_text=processed,
        required_skills=req_skills,
        required_experience=req_exp,
        required_education=req_edu,
    )


def extract_resume_info(
    file_path_or_text: str, candidate_id: Optional[Any] = None, category: Optional[str] = None
) -> ResumeInformation:
    """Extract structured information from a resume file path or raw text string.

    Args:
        file_path_or_text: File path (PDF/DOCX/TXT) or raw resume text.
        candidate_id: Optional identifier for candidate.
        category: Optional job category string.

    Returns:
        ResumeInformation dataclass.
    """
    raw_text = extract_text(file_path_or_text)
    cleaned_text = clean_raw_text(raw_text)
    processed_text = preprocess_text(raw_text)

    name = extract_name(raw_text)
    email = extract_email(raw_text)
    phone = extract_phone(raw_text)
    skills = extract_skills(raw_text)
    education = extract_education(raw_text)
    exp_years = extract_experience(raw_text)

    return ResumeInformation(
        raw_text=raw_text,
        cleaned_text=cleaned_text,
        processed_text=processed_text,
        id=candidate_id,
        category=category,
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        education=education,
        experience_years=exp_years,
    )


class ResumeScreeningPipeline:
    """End-to-end pipeline for processing resumes and ranking against job descriptions."""

    def __init__(self, scoring_weights: Optional[Dict[str, float]] = None):
        """Initialize pipeline with optional custom scoring weights."""
        self.scoring_weights = scoring_weights

    def process_and_rank(
        self,
        resumes: List[Union[str, Dict[str, Any]]],
        job_description_text: str,
    ) -> List[CandidateRankingResult]:
        """Batch process and rank multiple candidate resumes against a job description.

        Args:
            resumes: List of file paths, raw text strings, or dicts containing {'path'/'text', 'id', 'category'}.
            job_description_text: Raw job description text.

        Returns:
            List of CandidateRankingResult sorted by rank.
        """
        if not resumes:
            return []

        jd_info = analyze_job_description(job_description_text)

        # 1. Parse & Extract Resume Information
        resume_infos: List[ResumeInformation] = []
        for item in resumes:
            if isinstance(item, dict):
                src = item.get("path") or item.get("text") or item.get("resume_text") or ""
                c_id = item.get("id") or item.get("ID")
                cat = item.get("category") or item.get("Category")
                r_info = extract_resume_info(src, candidate_id=c_id, category=cat)
            else:
                r_info = extract_resume_info(item)
            resume_infos.append(r_info)

        # 2. Extract processed resume texts for embedding/tfidf matchers
        processed_resumes = [r.processed_text for r in resume_infos]

        # 3. Calculate TF-IDF Cosine Similarity
        tfidf_scores = compute_tfidf_similarity(
            jd_info.processed_text, processed_resumes
        )

        # 4. Calculate Semantic Cosine Similarity using Sentence Transformers
        semantic_scores = compute_semantic_similarity(
            jd_info.raw_text, processed_resumes
        )

        # 5. Build Matching Result per candidate
        matching_results: List[MatchingResult] = []
        for i, r_info in enumerate(resume_infos):
            matched_skills, missing_skills, skill_coverage = calculate_skill_match(
                r_info.skills, jd_info.required_skills
            )
            exp_score = calculate_experience_score(
                r_info.experience_years, jd_info.required_experience
            )

            m_result = MatchingResult(
                candidate_id=r_info.id,
                category=r_info.category,
                tfidf_score=float(tfidf_scores[i]) if i < len(tfidf_scores) else 0.0,
                semantic_score=float(semantic_scores[i]) if i < len(semantic_scores) else 0.0,
                matched_skills=matched_skills,
                missing_skills=missing_skills,
                skill_coverage=skill_coverage,
                experience_years=r_info.experience_years,
                experience_score=exp_score,
            )
            matching_results.append(m_result)

        # 6. Normalize Scores & Calculate Hybrid Scores
        updated_matching_results = compute_batch_hybrid_scores(
            matching_results, weights=self.scoring_weights
        )

        # 7. Sort & Rank Candidates
        pairs = list(zip(resume_infos, updated_matching_results))
        ranked_candidates = rank_candidates(pairs)

        return ranked_candidates


# Public pipeline functions for convenience
def process_resume(
    file_path_or_text: str,
    job_description_text: str,
    candidate_id: Optional[Any] = None,
) -> CandidateRankingResult:
    """Process a single resume against a job description.

    Args:
        file_path_or_text: File path or raw resume text.
        job_description_text: Job description text.
        candidate_id: Optional candidate ID.

    Returns:
        CandidateRankingResult for the candidate.
    """
    pipeline = ResumeScreeningPipeline()
    results = pipeline.process_and_rank(
        [{"text": file_path_or_text, "id": candidate_id}], job_description_text
    )
    return results[0]


def process_and_rank_candidates(
    resumes: List[Union[str, Dict[str, Any]]],
    job_description_text: str,
    scoring_weights: Optional[Dict[str, float]] = None,
) -> List[CandidateRankingResult]:
    """Process and rank multiple resumes against a job description.

    Args:
        resumes: List of file paths, texts, or dicts.
        job_description_text: Job description text.
        scoring_weights: Optional weights for hybrid score.

    Returns:
        List of CandidateRankingResult objects sorted by rank.
    """
    pipeline = ResumeScreeningPipeline(scoring_weights=scoring_weights)
    return pipeline.process_and_rank(resumes, job_description_text)
