"""Pydantic schemas for User registration, authentication, and responses."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Registration request schema."""
    name: str = Field(..., min_length=2, description="Full name of recruiter")
    email: EmailStr = Field(..., description="Recruiter email address")
    password: str = Field(..., min_length=8, description="Password (at least 8 characters)")


class LoginRequest(BaseModel):
    """Login credentials request schema."""
    email: EmailStr = Field(..., description="Recruiter email address")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    """JWT Token response schema."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Safe user profile response schema (NEVER contains password_hash)."""
    user_id: str
    name: str
    email: EmailStr
    role: str = "recruiter"
    is_active: bool = True
    created_at: Optional[datetime] = None
