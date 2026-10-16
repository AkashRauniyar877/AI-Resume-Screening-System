"""MongoDB Resume Document model helper."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional


def create_resume_document(
    resume_id: str,
    candidate_id: str,
    filename: str,
    file_type: str,
    extracted_text: str,
    original_filename: Optional[str] = None,
    stored_filename: Optional[str] = None,
    file_path: Optional[str] = None,
    content_type: Optional[str] = None,
    file_size: Optional[int] = 0,
) -> Dict[str, Any]:
    """Build a MongoDB document dictionary for a Resume.

    Args:
        resume_id: Unique resume identifier.
        candidate_id: Associated candidate identifier.
        filename: Original upload filename.
        file_type: Extension string (e.g. '.pdf').
        extracted_text: Cleaned extracted resume text.
        original_filename: Original file name.
        stored_filename: Safe name on disk.
        file_path: Physical path on disk.
        content_type: MIME type.
        file_size: File size in bytes.

    Returns:
        Dictionary document ready for MongoDB insertion.
    """
    orig_name = original_filename or filename
    return {
        "resume_id": resume_id,
        "candidate_id": candidate_id,
        "filename": orig_name,
        "original_filename": orig_name,
        "stored_filename": stored_filename or filename,
        "file_path": file_path or "",
        "content_type": content_type or "application/octet-stream",
        "file_size": int(file_size or 0),
        "file_type": file_type,
        "extracted_text": extracted_text,
        "created_at": datetime.now(timezone.utc),
        "upload_date": datetime.now(timezone.utc),
    }
