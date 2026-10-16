"""FastAPI authentication middleware and reusable JWT dependency."""

from typing import Any, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..utils.security import decode_access_token
from ..services.auth_service import AuthService

# Bearer token HTTP scheme for FastAPI OpenAPI /docs
security_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer),
) -> Dict[str, Any]:
    """FastAPI dependency to authenticate requests using JWT Bearer token.

    Args:
        credentials: Bearer token HTTP credentials.

    Returns:
        Authenticated user dictionary document from MongoDB.

    Raises:
        HTTPException: 401 Unauthorized if token is missing, invalid, or user inactive.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decode_access_token(token)

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token claims.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_service = AuthService()
    user = auth_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account no longer exists.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    return user
