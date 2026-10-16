"""FastAPI Application Entry Point for AI Resume Screening System backend."""

import os
import sys

# Add project root and backend directory to sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if os.path.dirname(BASE_DIR) not in sys.path:
    sys.path.insert(0, os.path.dirname(BASE_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.screening import router as screening_router
from backend.app.routes.auth import router as auth_router
from backend.app.routes.resumes import router as resumes_router

app = FastAPI(
    title="AI Resume Screening System API",
    description="FastAPI backend with JWT Authentication, MongoDB persistence, and AI screening pipeline.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(screening_router)
app.include_router(resumes_router)


@app.get("/", summary="Root Health Check")
def root():
    """Root endpoint verifying API server status."""
    return {
        "status": "online",
        "message": "AI Resume Screening System API is running.",
        "docs": "/docs",
    }


@app.get("/health", summary="Health Check")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
