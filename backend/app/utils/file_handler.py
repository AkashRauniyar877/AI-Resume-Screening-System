"""File upload utilities for temporary file handling and validation."""

import os
import tempfile
import shutil
from typing import List, Tuple
from fastapi import UploadFile, HTTPException, status

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


UPLOAD_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "resumes")
)

CONTENT_TYPE_MAP = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
}


def get_content_type(ext: str) -> str:
    """Get MIME content type for file extension."""
    return CONTENT_TYPE_MAP.get(ext.lower(), "application/octet-stream")


def validate_file_extension(filename: str) -> str:
    """Validate uploaded file extension.

    Args:
        filename: Name of uploaded file.

    Returns:
        Lowercased extension string (e.g., '.pdf').

    Raises:
        HTTPException: If extension is unsupported.
    """
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing.",
        )

    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{ext}'. Supported formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )
    return ext


def resolve_resume_path(file_path_or_name: str) -> str:
    """Safely resolve a stored filename, relative path, or legacy absolute path to an absolute path on disk.

    Args:
        file_path_or_name: Path or stored filename string from MongoDB.

    Returns:
        Absolute filepath string pointing to the physical file on disk.
    """
    if not file_path_or_name:
        return ""

    # Check if existing absolute path on disk (legacy records)
    if os.path.isabs(file_path_or_name) and os.path.exists(file_path_or_name):
        return os.path.abspath(file_path_or_name)

    filename = os.path.basename(file_path_or_name)
    target = os.path.join(UPLOAD_DIR, filename)
    return os.path.abspath(target)


def save_permanent_resume_file(upload_file: UploadFile, resume_id: str) -> dict:
    """Save an UploadFile object permanently into backend/uploads/resumes/ directory.

    Args:
        upload_file: FastAPI UploadFile object.
        resume_id: Unique resume identifier string.

    Returns:
        Dictionary containing file storage metadata with a portable relative file_path.
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = validate_file_extension(upload_file.filename)
    content_type = get_content_type(ext)

    # Reset file pointer and read bytes
    upload_file.file.seek(0)
    content = upload_file.file.read()
    upload_file.file.seek(0)

    if not content or len(content.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Uploaded file '{upload_file.filename}' is empty.",
        )

    stored_filename = f"resume_{resume_id}{ext}"
    abs_file_path = os.path.join(UPLOAD_DIR, stored_filename)

    with open(abs_file_path, "wb") as f:
        f.write(content)

    rel_file_path = f"uploads/resumes/{stored_filename}"

    return {
        "file_path": rel_file_path,
        "abs_file_path": abs_file_path,
        "stored_filename": stored_filename,
        "original_filename": upload_file.filename or stored_filename,
        "content_type": content_type,
        "file_size": len(content),
    }


def save_upload_to_temp_file(upload_file: UploadFile) -> str:
    """Save an UploadFile object to a temporary file on disk.

    Args:
        upload_file: FastAPI UploadFile object.

    Returns:
        Absolute filepath to the saved temporary file.
    """
    ext = validate_file_extension(upload_file.filename)

    # Read content to verify non-empty file
    upload_file.file.seek(0)
    content = upload_file.file.read()
    upload_file.file.seek(0)
    if not content or len(content.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Uploaded file '{upload_file.filename}' is empty.",
        )

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    try:
        temp_file.write(content)
        temp_file.flush()
        return temp_file.name
    finally:
        temp_file.close()


def cleanup_temp_file(filepath: str) -> None:
    """Safely remove a temporary file from disk.

    Args:
        filepath: Absolute filepath to delete.
    """
    if filepath and os.path.exists(filepath):
        try:
            os.remove(filepath)
        except OSError:
            pass

