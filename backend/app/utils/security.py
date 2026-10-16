"""Security utilities for password hashing and JWT token management."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import jwt
from pwdlib import PasswordHash
from fastapi import HTTPException, status
from ..config.settings import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
)

# Password hashing using pwdlib (Argon2 / Bcrypt)
_password_hasher = PasswordHash.recommended()


def validate_password(password: str) -> None:
    """Validate password strength (at least 8 characters).

    Raises:
        HTTPException: If password does not meet requirements.
    """
    if not password or len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long.",
        )


def hash_password(password: str) -> str:
    """Hash a plaintext password securely.

    Args:
        password: Plaintext password.

    Returns:
        Secure hash string.
    """
    validate_password(password)
    return _password_hasher.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify plaintext password against stored hash.

    Args:
        plain_password: Plaintext password.
        password_hash: Stored password hash string.

    Returns:
        True if password matches, False otherwise.
    """
    if not plain_password or not password_hash:
        return False
    try:
        return _password_hasher.verify(plain_password, password_hash)
    except Exception:
        return False


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a signed JWT access token.

    Args:
        data: Dictionary of claims to include in JWT payload.
        expires_delta: Optional timedelta expiration override.

    Returns:
        Encoded JWT token string.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT access token.

    Args:
        token: Encoded JWT token string.

    Returns:
        Decoded dictionary payload.

    Raises:
        HTTPException: If token is expired, invalid, or malformed.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
