"""FastAPI routes for viewing and downloading candidate resumes with JWT authorization."""

import os
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from backend.app.middleware.auth_middleware import get_current_user
from backend.app.services.resume_service import ResumeService
from backend.app.utils.file_handler import resolve_resume_path

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/resumes", tags=["Resumes"])


@router.get(
    "/{resume_id}/view",
    summary="View original resume inline (Authenticated)",
)
async def view_resume_endpoint(
    resume_id: str, current_user: dict = Depends(get_current_user)
):
    """Retrieve original uploaded resume file for inline viewing in browser tab."""
    service = ResumeService()
    recruiter_id = current_user.get("user_id")

    # 1. Fetch resume document metadata
    resume_doc = service.get_resume(resume_id)
    if not resume_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume record not found.",
        )

    # 2. Enforce recruiter ownership isolation
    if resume_doc.get("recruiter_id") and resume_doc.get("recruiter_id") != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this resume.",
        )

    raw_path = resume_doc.get("file_path") or resume_doc.get("stored_filename") or ""
    file_path = resolve_resume_path(raw_path)
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Physical resume file not found on server storage.",
        )

    orig_filename = resume_doc.get("original_filename") or resume_doc.get("filename") or f"{resume_id}.pdf"
    content_type = resume_doc.get("content_type") or "application/pdf"

    return FileResponse(
        path=file_path,
        media_type=content_type,
        headers={
            "Content-Disposition": f'inline; filename="{orig_filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get(
    "/{resume_id}/download",
    summary="Download original resume file (Authenticated)",
)
async def download_resume_endpoint(
    resume_id: str, current_user: dict = Depends(get_current_user)
):
    """Download original uploaded resume file as an attachment."""
    service = ResumeService()
    recruiter_id = current_user.get("user_id")

    # 1. Fetch resume document metadata
    resume_doc = service.get_resume(resume_id)
    if not resume_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume record not found.",
        )

    # 2. Enforce recruiter ownership isolation
    if resume_doc.get("recruiter_id") and resume_doc.get("recruiter_id") != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this resume.",
        )

    raw_path = resume_doc.get("file_path") or resume_doc.get("stored_filename") or ""
    file_path = resolve_resume_path(raw_path)
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Physical resume file not found on server storage.",
        )

    orig_filename = resume_doc.get("original_filename") or resume_doc.get("filename") or f"{resume_id}.pdf"
    content_type = resume_doc.get("content_type") or "application/octet-stream"

    return FileResponse(
        path=file_path,
        media_type=content_type,
        filename=orig_filename,
        headers={
            "Content-Disposition": f'attachment; filename="{orig_filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
