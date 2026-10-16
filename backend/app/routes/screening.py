"""FastAPI routes for resume parsing, screening, candidate ranking, and database queries.

Integrates directly with the ai_engine package, MongoDB services, and JWT authentication.
"""

import logging
import uuid
from typing import List, Optional
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Depends, status

from ai_engine import (
    extract_text,
    extract_resume_info,
    process_resume,
    process_and_rank_candidates,
    analyze_job_description,
)
from backend.app.schemas.screening_schema import (
    CandidateInfoSchema,
    ParseResumeResponse,
    SingleMatchResultSchema,
    ScreenResumeResponse,
    JobAnalysisSchema,
    RankedCandidateSchema,
    BatchScreenResponse,
)
from backend.app.utils.file_handler import (
    save_upload_to_temp_file,
    save_permanent_resume_file,
    resolve_resume_path,
    cleanup_temp_file,
)
from backend.app.middleware.auth_middleware import get_current_user
from backend.app.services.screening_service import ScreeningService
from backend.app.services.job_service import JobService
from backend.app.services.candidate_service import CandidateService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Screening"])


@router.post(
    "/parse-resume",
    response_model=ParseResumeResponse,
    status_code=status.HTTP_200_OK,
    summary="Parse raw resume file into text and structured information",
)
async def parse_resume_endpoint(file: UploadFile = File(...)):
    """Upload a PDF, DOCX, or TXT resume file to extract text and structured information."""
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded.",
        )

    temp_path = save_upload_to_temp_file(file)
    try:
        raw_text = extract_text(temp_path)
        info = extract_resume_info(temp_path)

        candidate_info = CandidateInfoSchema(
            name=info.name,
            email=info.email,
            phone=info.phone,
            skills=info.skills,
            education=info.education,
            experience_years=info.experience_years,
        )

        return ParseResumeResponse(
            filename=file.filename,
            extracted_text=raw_text,
            candidate_info=candidate_info,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing resume file: {str(e)}",
        )
    finally:
        cleanup_temp_file(temp_path)


@router.post(
    "/screen",
    response_model=ScreenResumeResponse,
    status_code=status.HTTP_200_OK,
    summary="Screen a single resume against a job description (Authenticated)",
)
async def screen_resume_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: Optional[str] = Form("Job Position"),
    current_user: dict = Depends(get_current_user),
):
    """Upload a resume file and job description text to screen candidate and compute scores under recruiter account."""
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resume file uploaded.",
        )

    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description cannot be empty.",
        )

    resume_id = uuid.uuid4().hex[:12]
    cand_id = f"cand_{resume_id}"
    file_metadata = save_permanent_resume_file(file, resume_id)
    perm_path = file_metadata.get("abs_file_path") or resolve_resume_path(file_metadata["file_path"])

    try:
        ranking_result = process_resume(perm_path, job_description, candidate_id=cand_id)
        ranking_result.resume_id = resume_id
        ranking_result.file_metadata = file_metadata

        jd_info = analyze_job_description(job_description)
        recruiter_id = current_user.get("user_id")

        # MongoDB persistence under recruiter ownership
        try:
            screening_svc = ScreeningService()
            screening_svc.save_batch_screening_to_mongo(
                job_title=job_title or "Job Position",
                job_description=job_description,
                jd_info_ai=jd_info,
                ranked_candidates=[ranking_result],
                recruiter_id=recruiter_id,
            )
        except Exception as mongo_err:
            logger.warning("MongoDB persistence skipped or failed: %s", str(mongo_err))

        res_info = ranking_result.resume_info
        m_result = ranking_result.matching_result

        cand_info = CandidateInfoSchema(
            name=res_info.name,
            email=res_info.email,
            phone=res_info.phone,
            skills=res_info.skills,
            education=res_info.education,
            experience_years=res_info.experience_years,
        )

        match_schema = SingleMatchResultSchema(
            matched_skills=m_result.matched_skills,
            missing_skills=m_result.missing_skills,
            skill_coverage=m_result.skill_coverage,
            tfidf_score=m_result.tfidf_score,
            tfidf_normalized=m_result.tfidf_normalized,
            semantic_score=m_result.semantic_score,
            semantic_normalized=m_result.semantic_normalized,
            experience_years=m_result.experience_years,
            experience_score=m_result.experience_score,
            hybrid_score=m_result.hybrid_score,
        )

        return ScreenResumeResponse(
            filename=file.filename,
            resume_id=resume_id,
            resume_actions={
                "view_url": f"/api/v1/resumes/{resume_id}/view",
                "download_url": f"/api/v1/resumes/{resume_id}/download",
            },
            candidate_info=cand_info,
            match_results=match_schema,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error screening candidate: {str(e)}",
        )


@router.post(
    "/screen-candidates",
    response_model=BatchScreenResponse,
    status_code=status.HTTP_200_OK,
    summary="Batch screen, rank, and persist multiple resumes against a job description (Authenticated)",
)
async def screen_candidates_endpoint(
    files: List[UploadFile] = File(...),
    job_description: str = Form(...),
    job_title: Optional[str] = Form("Job Position"),
    current_user: dict = Depends(get_current_user),
):
    """Upload multiple resume files and one job description to screen, rank, and store under recruiter account."""
    if not files or len(files) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one resume file must be uploaded.",
        )

    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description cannot be empty.",
        )

    resumes_input: List[dict] = []
    file_metadata_map: dict = {}

    try:
        for idx, file in enumerate(files):
            res_id = uuid.uuid4().hex[:12]
            cand_id = f"cand_{res_id}"
            file_meta = save_permanent_resume_file(file, res_id)

            resumes_input.append({
                "path": file_meta.get("abs_file_path") or resolve_resume_path(file_meta["file_path"]),
                "id": cand_id,
                "filename": file.filename,
                "resume_id": res_id,
                "file_metadata": file_meta,
            })
            file_metadata_map[cand_id] = (res_id, file_meta)

        # Process and rank candidates using existing ai_engine pipeline logic
        ranked_results = process_and_rank_candidates(resumes_input, job_description)

        for r_res in ranked_results:
            c_id = str(r_res.candidate_id)
            if c_id in file_metadata_map:
                r_res.resume_id = file_metadata_map[c_id][0]
                r_res.file_metadata = file_metadata_map[c_id][1]

        jd_info = analyze_job_description(job_description)
        recruiter_id = current_user.get("user_id")

        # Save to MongoDB associated with recruiter_id
        try:
            screening_svc = ScreeningService()
            screening_svc.save_batch_screening_to_mongo(
                job_title=job_title or "Job Position",
                job_description=job_description,
                jd_info_ai=jd_info,
                ranked_candidates=ranked_results,
                recruiter_id=recruiter_id,
            )
        except Exception as mongo_err:
            logger.warning("MongoDB batch persistence skipped or failed: %s", str(mongo_err))

        jd_schema = JobAnalysisSchema(
            required_skills=jd_info.required_skills,
            required_experience=jd_info.required_experience,
            required_education=jd_info.required_education,
        )

        ranked_schemas: List[RankedCandidateSchema] = []
        for r_res in ranked_results:
            cand_info = CandidateInfoSchema(
                name=r_res.resume_info.name,
                email=r_res.resume_info.email,
                phone=r_res.resume_info.phone,
                skills=r_res.resume_info.skills,
                education=r_res.resume_info.education,
                experience_years=r_res.resume_info.experience_years,
            )

            m_result = r_res.matching_result
            match_schema = SingleMatchResultSchema(
                matched_skills=m_result.matched_skills,
                missing_skills=m_result.missing_skills,
                skill_coverage=m_result.skill_coverage,
                tfidf_score=m_result.tfidf_score,
                tfidf_normalized=m_result.tfidf_normalized,
                semantic_score=m_result.semantic_score,
                semantic_normalized=m_result.semantic_normalized,
                experience_years=m_result.experience_years,
                experience_score=m_result.experience_score,
                hybrid_score=m_result.hybrid_score,
            )

            res_id_val = getattr(r_res, "resume_id", None) or f"res_{r_res.candidate_id}"
            ranked_schemas.append(
                RankedCandidateSchema(
                    rank=r_res.rank,
                    candidate_id=r_res.candidate_id,
                    resume_id=res_id_val,
                    filename=str(r_res.candidate_id),
                    hybrid_score=r_res.hybrid_score,
                    candidate_info=cand_info,
                    match_results=match_schema,
                    resume_actions={
                        "view_url": f"/api/v1/resumes/{res_id_val}/view",
                        "download_url": f"/api/v1/resumes/{res_id_val}/download",
                    },
                )
            )

        return BatchScreenResponse(
            total_candidates=len(ranked_schemas),
            job_description_analysis=jd_schema,
            ranked_candidates=ranked_schemas,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in batch screening candidates: {str(e)}",
        )


@router.get("/jobs", summary="List stored jobs for authenticated recruiter")
def list_jobs_endpoint(current_user: dict = Depends(get_current_user)):
    """Retrieve all jobs stored in MongoDB belonging to the authenticated recruiter."""
    try:
        service = JobService()
        return service.list_jobs(recruiter_id=current_user["user_id"])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching jobs: {str(e)}",
        )


@router.get("/jobs/{job_id}/results", summary="Get ranked candidate screening results for a job (Authenticated)")
def get_job_results_endpoint(
    job_id: str, current_user: dict = Depends(get_current_user)
):
    """Retrieve stored candidate screening results for a specific job_id, verifying recruiter ownership."""
    try:
        service = ScreeningService()
        results = service.get_screening_results_for_job(
            job_id, recruiter_id=current_user["user_id"]
        )
        return {"job_id": job_id, "results_count": len(results), "results": results}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching screening results: {str(e)}",
        )


@router.get("/candidates", summary="List saved candidates for authenticated recruiter")
def list_candidates_endpoint(current_user: dict = Depends(get_current_user)):
    """Retrieve candidates saved in MongoDB belonging to the authenticated recruiter."""
    try:
        service = CandidateService()
        return service.list_candidates(recruiter_id=current_user["user_id"])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching candidates: {str(e)}",
        )
