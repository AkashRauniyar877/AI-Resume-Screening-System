"""Skill extraction module."""

import re
from typing import List, Optional

from ..config.ai_config import DEFAULT_SKILLS


SKILL_ALIASES = {
    "javascript": [
        "javascript",
        "java script",
        "js",
    ], 
    "java": [
        "java",
    ],
    "c++": [
        "c++",
        "cpp",
        "c/c++",
    ],
    "html": [
        "html",
        "html5",
    ],
    "css": [
        "css",
        "css3",
    ],
    "react": [
        "react",
        "react.js",
        "reactjs",
        "react js",
    ],
    "node.js": [
        "node.js",
        "nodejs",
        "node js",
    ],
    "express": [
        "express",
        "express.js",
        "expressjs",
    ],
    "mongodb": [
        "mongodb",
        "mongo db",
    ],
    "mysql": [
        "mysql",
        "my sql",
    ],
    "postgresql": [
        "postgresql",
        "postgres",
    ],
    "github": [
        "github",
        "git hub",
    ],
    "vs code": [
        "vs code",
        "visual studio code",
    ],
    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
    ],
    "object oriented programming": [
        "object oriented programming",
        "object-oriented programming",
        "oop",
    ],
    "dbms": [
        "dbms",
        "database management systems",
        "database management system",
    ],
    "data structures and algorithms": [
        "data structures and algorithms",
        "data structure and algorithms",
        "data structures & algorithms",
        "data structure & algorithms",
    ],
    "operating systems": [
        "operating systems",
        "operating system",
    ],
    "computer networks": [
        "computer networks",
        "computer network",
    ],
    "machine learning": [
        "machine learning",
    ],
    "natural language processing": [
        "natural language processing",
        "nlp",
    ],
    "gemini api": [
        "gemini api",
    ],
    "easyocr": [
        "easyocr",
    ],
    "apscheduler": [
        "apscheduler",
    ],
}


def _contains_skill(text: str, skill: str) -> bool:
    """Check whether a skill exists as a complete term."""
    escaped = re.escape(skill)

    pattern = rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])"

    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(
    text: str,
    skills_list: Optional[List[str]] = None
) -> List[str]:
    """Extract canonical skills from resume/JD text."""

    if not isinstance(text, str) or not text.strip():
        return []

    text_lower = text.lower()

    if skills_list is None:
        skills_list = DEFAULT_SKILLS

    found_skills = []

    # First detect canonical skills through aliases.
    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:
            if _contains_skill(text_lower, alias):
                found_skills.append(canonical_skill)
                break

    # Detect normal skills that don't have aliases.
    for skill in skills_list:

        skill_lower = skill.lower()

        if skill_lower in SKILL_ALIASES:
            continue

        if _contains_skill(text_lower, skill_lower):
            found_skills.append(skill_lower)

    # Remove duplicates while preserving order.
    unique_skills = []

    for skill in found_skills:
        if skill not in unique_skills:
            unique_skills.append(skill)

    # Remove generic/component skills when a more specific
    # canonical skill already represents them.
    covered_skills = {
        "rest api": {"rest", "api"},
        "object oriented programming": {"oop"},
        "data structures and algorithms": {
            "data structures",
            "algorithms",
        },
        "natural language processing": {"nlp"},
    }

    final_skills = []

    for skill in unique_skills:

        # If this skill is a component of a more specific skill
        # that was already detected, skip it.
        skip = False

        for main_skill, component_skills in covered_skills.items():

            if skill in component_skills and main_skill in unique_skills:
                skip = True
                break

        if not skip:
            final_skills.append(skill)

    return final_skills