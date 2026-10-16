"""Database service layer for Recruiter Authentication and User Management."""

from typing import Any, Dict, Optional
from pymongo.database import Database
from fastapi import HTTPException, status
from ..config.database import get_database
from ..models.user import create_user_document
from ..utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    validate_password,
)


class AuthService:
    """Service class handling User Registration, Authentication, and MongoDB Queries."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db if db is not None else get_database()

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve user document by email address.

        Args:
            email: User email address.

        Returns:
            User dictionary document or None.
        """
        if not email:
            return None
        clean_email = email.strip().lower()
        doc = self.db["users"].find_one({"email": clean_email})
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user document by user_id string.

        Args:
            user_id: Unique user identifier.

        Returns:
            User dictionary document or None.
        """
        if not user_id:
            return None
        doc = self.db["users"].find_one({"user_id": user_id})
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def register_user(
        self, name: str, email: str, password: str, role: str = "recruiter"
    ) -> Dict[str, Any]:
        """Register a new recruiter user account.

        Args:
            name: Recruiter full name.
            email: Recruiter email.
            password: Plaintext password.
            role: Account role (default: recruiter).

        Returns:
            Safe user profile dictionary without password_hash.

        Raises:
            HTTPException: 409 Conflict if email exists, 400 Bad Request if weak password.
        """
        validate_password(password)
        clean_email = email.strip().lower()

        # Check if email is already registered
        existing = self.get_user_by_email(clean_email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email address already exists.",
            )

        pass_hash = hash_password(password)
        doc = create_user_document(
            name=name,
            email=clean_email,
            password_hash=pass_hash,
            role=role,
        )

        result = self.db["users"].insert_one(doc)
        doc["_id"] = str(result.inserted_id)

        # Remove password_hash before returning safe user object
        doc.pop("password_hash", None)
        return doc

    def authenticate_user(self, email: str, password: str) -> Dict[str, str]:
        """Authenticate user credentials and generate JWT access token.

        Args:
            email: User email address.
            password: Plaintext password.

        Returns:
            Dictionary containing access_token and token_type.

        Raises:
            HTTPException: 401 Unauthorized for invalid credentials, 403 Forbidden for inactive account.
        """
        user = self.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive. Please contact administrator.",
            )

        token_data = {
            "sub": user["user_id"],
            "email": user["email"],
            "role": user.get("role", "recruiter"),
        }
        access_token = create_access_token(data=token_data)

        return {"access_token": access_token, "token_type": "bearer"}
