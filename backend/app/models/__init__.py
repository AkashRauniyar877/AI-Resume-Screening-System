"""Models package initialization."""

from .job import create_job_document
from .candidate import create_candidate_document
from .resume import create_resume_document
from .screening_result import create_screening_result_document
from .user import create_user_document

__all__ = [
    "create_job_document",
    "create_candidate_document",
    "create_resume_document",
    "create_screening_result_document",
    "create_user_document",
]
