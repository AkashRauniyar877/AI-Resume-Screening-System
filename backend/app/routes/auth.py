"""FastAPI routes for Recruiter registration, authentication, and profile retrieval."""

from fastapi import APIRouter, Depends, status
from backend.app.schemas.user_schema import (
    UserRegister,
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from backend.app.services.auth_service import AuthService
from backend.app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new recruiter account",
)
def register_endpoint(payload: UserRegister):
    """Register a new recruiter account with name, email, and password."""
    auth_service = AuthService()
    user = auth_service.register_user(
        name=payload.name,
        email=payload.email,
        password=payload.password,
    )
    return UserResponse(
        user_id=user["user_id"],
        name=user["name"],
        email=user["email"],
        role=user.get("role", "recruiter"),
        is_active=user.get("is_active", True),
        created_at=user.get("created_at"),
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login recruiter and issue JWT access token",
)
def login_endpoint(payload: LoginRequest):
    """Authenticate recruiter with email and password to receive a JWT access token."""
    auth_service = AuthService()
    token_dict = auth_service.authenticate_user(
        email=payload.email,
        password=payload.password,
    )
    return TokenResponse(
        access_token=token_dict["access_token"],
        token_type=token_dict["token_type"],
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated recruiter profile",
)
def get_me_endpoint(current_user: dict = Depends(get_current_user)):
    """Retrieve details for the currently authenticated recruiter."""
    return UserResponse(
        user_id=current_user["user_id"],
        name=current_user["name"],
        email=current_user["email"],
        role=current_user.get("role", "recruiter"),
        is_active=current_user.get("is_active", True),
        created_at=current_user.get("created_at"),
    )
