"""Database service layer for Resumes with recruiter data isolation."""

from typing import Any, Dict, Optional
from pymongo.database import Database
from ..config.database import get_database
from ..models.resume import create_resume_document


class ResumeService:
    """Service class handling Resume metadata operations in MongoDB."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db if db is not None else get_database()

    def create_resume(
        self,
        resume_id: str,
        candidate_id: str,
        filename: str,
        file_type: str,
        extracted_text: str,
        recruiter_id: Optional[str] = None,
        original_filename: Optional[str] = None,
        stored_filename: Optional[str] = None,
        file_path: Optional[str] = None,
        content_type: Optional[str] = None,
        file_size: Optional[int] = 0,
    ) -> Dict[str, Any]:
        """Insert a resume metadata document."""
        doc = create_resume_document(
            resume_id=resume_id,
            candidate_id=candidate_id,
            filename=filename,
            file_type=file_type,
            extracted_text=extracted_text,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_path=file_path,
            content_type=content_type,
            file_size=file_size,
        )
        if recruiter_id:
            doc["recruiter_id"] = recruiter_id

        self.db["resumes"].update_one(
            {"resume_id": resume_id},
            {"$set": doc},
            upsert=True,
        )
        saved = self.db["resumes"].find_one({"resume_id": resume_id})
        if saved and "_id" in saved:
            saved["_id"] = str(saved["_id"])
        return saved or doc

    def get_resume(
        self, resume_id: str, recruiter_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Retrieve resume document by resume_id."""
        query: Dict[str, Any] = {"resume_id": resume_id}
        if recruiter_id:
            query["recruiter_id"] = recruiter_id
        doc = self.db["resumes"].find_one(query)
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc
