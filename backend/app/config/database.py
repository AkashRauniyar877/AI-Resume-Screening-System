"""MongoDB Database connection and collection management using PyMongo."""

import logging
from typing import Optional
import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import OperationFailure
from .settings import MONGODB_URI, MONGODB_DB_NAME

logger = logging.getLogger(__name__)

_mongo_client: Optional[MongoClient] = None
_db: Optional[Database] = None


def get_mongo_client() -> MongoClient:
    """Get or create singleton PyMongo client instance."""
    global _mongo_client
    if _mongo_client is None:
        try:
            _mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            # Verify connection
            _mongo_client.admin.command("ping")
            logger.info("Successfully connected to MongoDB at %s", MONGODB_URI)
        except Exception as e:
            logger.error("Failed to connect to MongoDB: %s", str(e))
            raise e
    return _mongo_client


def get_database(db_name: Optional[str] = None) -> Database:
    """Get database handle.

    Args:
        db_name: Optional database name override.

    Returns:
        PyMongo Database object.
    """
    global _db
    target_name = db_name or MONGODB_DB_NAME
    if _db is None or _db.name != target_name:
        client = get_mongo_client()
        _db = client[target_name]
        init_db_indexes(_db)
    return _db


def _safe_create_index(collection, keys, **kwargs):
    try:
        collection.create_index(keys, **kwargs)
    except OperationFailure:
        pass
    except Exception as e:
        logger.debug("Index creation note for %s: %s", collection.name, str(e))


def init_db_indexes(db: Database) -> None:
    """Initialize essential MongoDB collection indexes."""
    try:
        # Users collection indexes (Recruiter accounts)
        _safe_create_index(db["users"], "email", unique=True)
        _safe_create_index(db["users"], "user_id", unique=True)

        # Jobs collection index (including recruiter_id filter)
        _safe_create_index(db["jobs"], [("created_at", pymongo.DESCENDING)])
        _safe_create_index(db["jobs"], "recruiter_id")

        # Candidates collection indexes
        _safe_create_index(db["candidates"], "candidate_id")
        _safe_create_index(db["candidates"], "email", sparse=True)
        _safe_create_index(db["candidates"], "recruiter_id")

        # Resumes collection indexes
        _safe_create_index(db["resumes"], "resume_id")
        _safe_create_index(db["resumes"], "candidate_id")
        _safe_create_index(db["resumes"], "recruiter_id")

        # Screening Results collection indexes
        _safe_create_index(db["screening_results"], "job_id")
        _safe_create_index(db["screening_results"], "candidate_id")
        _safe_create_index(db["screening_results"], "recruiter_id")
        _safe_create_index(db["screening_results"], [("job_id", pymongo.ASCENDING), ("rank", pymongo.ASCENDING)])
        _safe_create_index(db["screening_results"], [("job_id", pymongo.ASCENDING), ("hybrid_score", pymongo.DESCENDING)])

        logger.info("MongoDB collection indexes initialized successfully.")
    except Exception as e:
        logger.warning("Could not initialize MongoDB indexes: %s", str(e))


def close_mongo_connection() -> None:
    """Close PyMongo client connection."""
    global _mongo_client, _db
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        _db = None
        logger.info("MongoDB connection closed.")
