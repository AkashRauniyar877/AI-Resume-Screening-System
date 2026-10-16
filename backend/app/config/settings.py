"""Application configuration and settings module."""

import os
from dotenv import load_dotenv

# Load environment variables from backend/.env if present
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "ai_resume_screening_db")
DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", "8000"))

# JWT Security Settings
JWT_SECRET_KEY: str = os.getenv(
    "JWT_SECRET_KEY", "c87d4a6f91e3b52d0a4c8e1f7b9a3d5c2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b"
)
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
