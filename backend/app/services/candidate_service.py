"""Database service layer for Candidates with recruiter data isolation."""

from typing import Any, Dict, List, Optional
from pymongo import ReturnDocument
from pymongo.database import Database
from ..config.database import get_database
from ..models.candidate import create_candidate_document


class CandidateService:
    """Service class handling Candidate document operations in MongoDB."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db if db is not None else get_database()

    def create_or_update_candidate(
        self,
        candidate_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        skills: Optional[List[str]] = None,
        education: Optional[List[str]] = None,
        experience_years: float = 0.0,
        recruiter_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Insert a candidate document or update if candidate_id already exists."""
        doc = create_candidate_document(
            candidate_id=candidate_id,
            name=name,
            email=email,
            phone=phone,
            skills=skills,
            education=education,
            experience_years=experience_years,
        )
        if recruiter_id:
            doc["recruiter_id"] = recruiter_id

        result = self.db["candidates"].find_one_and_update(
            {"candidate_id": candidate_id},
            {"$set": doc},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        if result and "_id" in result:
            result["_id"] = str(result["_id"])
        return result or doc

    def get_candidate(
        self, candidate_id: str, recruiter_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Find candidate by candidate_id and optional recruiter_id."""
        query: Dict[str, Any] = {"candidate_id": candidate_id}
        if recruiter_id:
            query["recruiter_id"] = recruiter_id
        doc = self.db["candidates"].find_one(query)
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def list_candidates(
        self, recruiter_id: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List candidates filtered by recruiter_id."""
        query = {}
        if recruiter_id:
            query["recruiter_id"] = recruiter_id

        cursor = self.db["candidates"].find(query).sort("created_at", -1).limit(limit)
        candidates = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            candidates.append(doc)
        return candidates
