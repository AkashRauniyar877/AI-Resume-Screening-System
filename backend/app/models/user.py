"""MongoDB User Document model helper for Recruiter accounts."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def create_user_document(
    name: str,
    email: str,
    password_hash: str,
    role: str = "recruiter",
    is_active: bool = True,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a MongoDB document dictionary for a Recruiter User.

    Args:
        name: Full name of recruiter.
        email: Lowercased email address.
        password_hash: Securely hashed password (NEVER plaintext).
        role: User role (default: recruiter).
        is_active: Account status (default: True).
        user_id: Optional unique user identifier (UUID generated if None).

    Returns:
        Dictionary document ready for MongoDB insertion into 'users' collection.
    """
    return {
        "user_id": user_id or f"usr_{uuid.uuid4().hex[:16]}",
        "name": name.strip(),
        "email": email.strip().lower(),
        "password_hash": password_hash,
        "role": role,
        "is_active": is_active,
        "created_at": datetime.now(timezone.utc),
    }
