"""Database service layer for Job postings with recruiter data isolation."""

from typing import Any, Dict, List, Optional
from bson import ObjectId
from pymongo.database import Database
from ..config.database import get_database
from ..models.job import create_job_document


class JobService:
    """Service class handling CRUD operations for Jobs in MongoDB."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db if db is not None else get_database()

    def create_job(
        self,
        job_title: str,
        job_description: str,
        required_skills: Optional[List[str]] = None,
        required_experience: float = 0.0,
        required_education: Optional[List[str]] = None,
        recruiter_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create and store a new Job document associated with recruiter_id."""
        doc = create_job_document(
            job_title=job_title,
            job_description=job_description,
            required_skills=required_skills,
            required_experience=required_experience,
            required_education=required_education,
        )
        if recruiter_id:
            doc["recruiter_id"] = recruiter_id

        result = self.db["jobs"].insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc

    def get_job_by_id(
        self, job_id: str, recruiter_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Retrieve job document by ID string or ObjectId, filtering by recruiter_id if provided."""
        try:
            query: Dict[str, Any] = (
                {"_id": ObjectId(job_id)} if ObjectId.is_valid(job_id) else {"_id": job_id}
            )
            if recruiter_id:
                query["recruiter_id"] = recruiter_id

            doc = self.db["jobs"].find_one(query)
            if doc:
                doc["_id"] = str(doc["_id"])
            return doc
        except Exception:
            return None

    def list_jobs(
        self, recruiter_id: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List job postings sorted by created_at descending, filtered by recruiter_id."""
        query = {}
        if recruiter_id:
            query["recruiter_id"] = recruiter_id

        cursor = self.db["jobs"].find(query).sort("created_at", -1).limit(limit)
        jobs = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            jobs.append(doc)
        return jobs
