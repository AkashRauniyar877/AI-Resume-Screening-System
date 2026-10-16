"""Database service layer for Screening Results and Batch Workflow Coordination with recruiter authorization."""

from typing import Any, Dict, List, Optional
import os
from pymongo.database import Database
from fastapi import HTTPException, status
from ..config.database import get_database
from ..models.screening_result import create_screening_result_document
from .job_service import JobService
from .candidate_service import CandidateService
from .resume_service import ResumeService


class ScreeningService:
    """Service class handling screening result storage and retrieval in MongoDB."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db if db is not None else get_database()
        self.job_service = JobService(self.db)
        self.candidate_service = CandidateService(self.db)
        self.resume_service = ResumeService(self.db)

    def save_screening_result(
        self,
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
        recruiter_id: Optional[str] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        education: Optional[List[str]] = None,
        experience_years: Optional[float] = 0.0,
        skills: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Save candidate screening result document in MongoDB."""
        doc = create_screening_result_document(
            job_id=job_id,
            candidate_id=candidate_id,
            resume_id=resume_id,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            skill_coverage=skill_coverage,
            tfidf_score=tfidf_score,
            tfidf_normalized=tfidf_normalized,
            semantic_score=semantic_score,
            semantic_normalized=semantic_normalized,
            experience_score=experience_score,
            hybrid_score=hybrid_score,
            rank=rank,
            name=name,
            email=email,
            phone=phone,
            education=education,
            experience_years=experience_years,
            skills=skills,
        )
        if recruiter_id:
            doc["recruiter_id"] = recruiter_id

        self.db["screening_results"].update_one(
            {"job_id": job_id, "candidate_id": candidate_id},
            {"$set": doc},
            upsert=True,
        )
        saved = self.db["screening_results"].find_one({"job_id": job_id, "candidate_id": candidate_id})
        if saved and "_id" in saved:
            saved["_id"] = str(saved["_id"])
        return saved or doc

    def get_screening_results_for_job(
        self, job_id: str, recruiter_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve ranked screening results for a specific job_id, verifying job ownership."""
        # 1. Verify job ownership if recruiter_id is specified
        if recruiter_id:
            job = self.job_service.get_job_by_id(job_id)
            if not job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job posting not found.",
                )
            if job.get("recruiter_id") != recruiter_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not authorized to view results for this job.",
                )

        query = {"job_id": job_id}
        cursor = self.db["screening_results"].find(query).sort("rank", 1)
        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])

            # Look up candidate details if missing in doc
            if not doc.get("name") and not doc.get("email"):
                cand_doc = self.candidate_service.get_candidate(doc.get("candidate_id", ""))
                if cand_doc:
                    doc["name"] = cand_doc.get("name")
                    doc["email"] = cand_doc.get("email")
                    doc["phone"] = cand_doc.get("phone")
                    doc["education"] = cand_doc.get("education", [])
                    doc["experience_years"] = cand_doc.get("experience_years", 0.0)
                    doc["skills"] = cand_doc.get("skills", [])

            # Construct candidate_info, match_results, and resume_actions sub-objects for API schema consistency
            doc["candidate_info"] = {
                "name": doc.get("name"),
                "email": doc.get("email"),
                "phone": doc.get("phone"),
                "education": doc.get("education") or [],
                "experience_years": float(doc.get("experience_years") or 0.0),
                "skills": doc.get("skills") or [],
            }
            doc["match_results"] = {
                "matched_skills": doc.get("matched_skills") or [],
                "missing_skills": doc.get("missing_skills") or [],
                "skill_coverage": float(doc.get("skill_coverage") or 0.0),
                "tfidf_score": float(doc.get("tfidf_score") or 0.0),
                "tfidf_normalized": float(doc.get("tfidf_normalized") or 0.0),
                "semantic_score": float(doc.get("semantic_score") or 0.0),
                "semantic_normalized": float(doc.get("semantic_normalized") or 0.0),
                "experience_years": float(doc.get("experience_years") or 0.0),
                "experience_score": float(doc.get("experience_score") or 0.0),
                "hybrid_score": float(doc.get("hybrid_score") or 0.0),
            }
            r_id = doc.get("resume_id")
            if r_id:
                doc["resume_actions"] = {
                    "view_url": f"/api/v1/resumes/{r_id}/view",
                    "download_url": f"/api/v1/resumes/{r_id}/download",
                }

            results.append(doc)
        return results

    def save_batch_screening_to_mongo(
        self,
        job_title: str,
        job_description: str,
        jd_info_ai: Any,
        ranked_candidates: List[Any],
        recruiter_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Persist job, candidates, resumes, and screening results into MongoDB under recruiter ownership.

        Args:
            job_title: Title of job posting.
            job_description: Job description text.
            jd_info_ai: JobDescriptionInformation from ai_engine.
            ranked_candidates: List of CandidateRankingResult from ai_engine.
            recruiter_id: Authenticated recruiter user_id.

        Returns:
            Dictionary containing stored job_id and record counts.
        """
        # 1. Store Job Document associated with recruiter_id
        job_doc = self.job_service.create_job(
            job_title=job_title,
            job_description=job_description,
            required_skills=jd_info_ai.required_skills,
            required_experience=jd_info_ai.required_experience,
            required_education=jd_info_ai.required_education,
            recruiter_id=recruiter_id,
        )
        job_id = str(job_doc["_id"])

        stored_count = 0
        for cand_rank_result in ranked_candidates:
            res_info = cand_rank_result.resume_info
            m_res = cand_rank_result.matching_result

            c_id = str(cand_rank_result.candidate_id or res_info.id or f"cand_{cand_rank_result.rank}")
            r_id = getattr(cand_rank_result, "resume_id", None) or f"res_{c_id}"

            # Extract optional file metadata attached during endpoint processing
            file_meta = getattr(cand_rank_result, "file_metadata", {}) or {}
            orig_filename = file_meta.get("original_filename") or str(cand_rank_result.candidate_id)
            stored_filename = file_meta.get("stored_filename") or orig_filename
            f_path = file_meta.get("file_path") or ""
            c_type = file_meta.get("content_type") or "application/octet-stream"
            f_size = file_meta.get("file_size") or 0

            # 2. Store Candidate Document
            self.candidate_service.create_or_update_candidate(
                candidate_id=c_id,
                name=res_info.name,
                email=res_info.email,
                phone=res_info.phone,
                skills=res_info.skills,
                education=res_info.education,
                experience_years=res_info.experience_years,
                recruiter_id=recruiter_id,
            )

            # 3. Store Resume Document
            filename = orig_filename
            ext = os.path.splitext(filename)[1].lower() if "." in filename else ".txt"
            self.resume_service.create_resume(
                resume_id=r_id,
                candidate_id=c_id,
                filename=filename,
                file_type=ext,
                extracted_text=res_info.cleaned_text or res_info.raw_text,
                recruiter_id=recruiter_id,
                original_filename=orig_filename,
                stored_filename=stored_filename,
                file_path=f_path,
                content_type=c_type,
                file_size=f_size,
            )

            # 4. Store Screening Result Document
            self.save_screening_result(
                job_id=job_id,
                candidate_id=c_id,
                resume_id=r_id,
                matched_skills=m_res.matched_skills,
                missing_skills=m_res.missing_skills,
                skill_coverage=m_res.skill_coverage,
                tfidf_score=m_res.tfidf_score,
                tfidf_normalized=m_res.tfidf_normalized,
                semantic_score=m_res.semantic_score,
                semantic_normalized=m_res.semantic_normalized,
                experience_score=m_res.experience_score,
                hybrid_score=m_res.hybrid_score,
                rank=cand_rank_result.rank,
                recruiter_id=recruiter_id,
                name=res_info.name,
                email=res_info.email,
                phone=res_info.phone,
                education=res_info.education,
                experience_years=res_info.experience_years,
                skills=res_info.skills,
            )
            stored_count += 1

        return {"job_id": job_id, "stored_count": stored_count}
