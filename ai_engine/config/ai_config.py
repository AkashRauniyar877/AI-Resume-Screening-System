"""Configuration module for AI Resume Screening System.

Stores skill definitions, regex patterns, scoring weights, and model configurations.
"""

from typing import Dict, List, Pattern
import re

# Complete 43-skill list from Notebook 04 & 10
DEFAULT_SKILLS: List[str] = [
    # Programming Languages
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",

    # Web
    "html",
    "css",
    "react",
    "node.js",
    "express",

    # Backend / APIs
    "fastapi",
    "flask",
    "django",
    "rest api",
    "rest",
    "api",
    "jdbc",

    # Databases
    "sql",
    "mysql",
    "mongodb",
    "postgresql",
    "oracle",
    "redis",

    # Version Control / Tools
    "git",
    "github",
    "docker",
    "vs code",

    # Cloud
    "aws",
    "azure",

    # Operating Systems
    "linux",
    "operating systems",

    # Data / Analytics
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "scikit-learn",
    "data analysis",
    "data visualization",

    # AI / ML
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "tensorflow",
    "pytorch",

    # Computer Science Fundamentals
    "data structures",
    "algorithms",
    "object oriented programming",
    "oop",
    "dbms",
    "database management systems",
    "computer networks",

    # AI / Other Tools
    "gemini api",
    "easyocr",
    "apscheduler",
]

# Education regex patterns from Notebook 09 & 10
EDUCATION_PATTERNS: List[str] = [
    r"\bB\.?Tech\b",
    r"\bB\.?E\.?\b",
    r"\bB\.?Sc\.?\b",
    r"\bB\.?A\.?\b",
    r"\bB\.?Com\.?\b",
    r"\bBCA\b",
    r"\bMCA\b",
    r"\bM\.?Tech\b",
    r"\bM\.?E\.?\b",
    r"\bM\.?Sc\.?\b",
    r"\bM\.?A\.?\b",
    r"\bM\.?Com\.?\b",
    r"\bMBA\b",
    r"\bPh\.?D\.?\b",
    r"\bBachelor'?s degree\b",
    r"\bMaster'?s degree\b",
    r"\bBachelor of (?:Arts|Science|Engineering|Technology|Education|Commerce|Business Administration|Computer Applications)\b",
    r"\bMaster of (?:Arts|Science|Engineering|Technology|Education|Business Administration|Public Administration|Commerce|Computer Applications)\b"
]

# Hybrid scoring weights from Notebook 08
DEFAULT_SCORING_WEIGHTS: Dict[str, float] = {
    "skill": 0.35,
    "semantic": 0.30,
    "tfidf": 0.20,
    "experience": 0.15
}

# Sentence Transformer model configuration from Notebook 07
SEMANTIC_MODEL_NAME: str = "all-MiniLM-L6-v2"

# Supported file extensions for resume parsing
SUPPORTED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt"]
