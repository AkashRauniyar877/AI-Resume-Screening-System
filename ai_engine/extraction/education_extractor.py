"""Education extraction module.

Implements degree regex matching and normalization matching Notebook 09 & 10.
"""

import re
from typing import List, Optional
from ..config.ai_config import EDUCATION_PATTERNS


def normalize_education(education_list: List[str]) -> List[str]:
    """Normalize extracted education degree titles.

    Args:
        education_list: List of raw extracted degree strings.

    Returns:
        List of normalized unique degree strings.
    """
    normalized = []
    for edu in education_list:
        clean_edu = edu.lower().strip()
        clean_no_punct = re.sub(r"[^\w\s]", "", clean_edu)

        if clean_no_punct in ["bachelor of science", "bsc"]:
            formatted = "Bachelor of Science"
        elif clean_no_punct in ["bachelor of arts", "ba"]:
            formatted = "Bachelor of Arts"
        elif clean_no_punct in ["master of science", "msc"]:
            formatted = "Master of Science"
        elif clean_no_punct in ["master of arts", "ma"]:
            formatted = "Master of Arts"
        elif clean_no_punct in ["bachelor of engineering", "be"]:
            formatted = "Bachelor of Engineering"
        elif clean_no_punct in ["bachelor of technology", "btech"]:
            formatted = "Bachelor of Technology"
        elif clean_no_punct in ["bachelor of commerce", "bcom"]:
            formatted = "Bachelor of Commerce"
        elif clean_no_punct in ["bachelor of computer applications", "bca"]:
            formatted = "BCA"
        elif clean_no_punct in ["master of computer applications", "mca"]:
            formatted = "MCA"
        elif clean_no_punct in ["bachelor of business administration", "bba"]:
            formatted = "Bachelor of Business Administration"
        elif clean_no_punct in ["master of business administration", "mba"]:
            formatted = "MBA"
        elif clean_no_punct in ["master of engineering", "me"]:
            formatted = "Master of Engineering"
        elif clean_no_punct in ["master of technology", "mtech"]:
            formatted = "Master of Technology"
        elif clean_no_punct in ["bachelors degree", "bachelor degree"]:
            formatted = "Bachelor's degree"
        elif clean_no_punct in ["masters degree", "master degree"]:
            formatted = "Master's degree"
        elif clean_no_punct in ["phd"]:
            formatted = "Ph.D."
        else:
            formatted = edu.strip()

        if formatted not in normalized:
            normalized.append(formatted)

    return normalized


def extract_education(text: str, patterns: Optional[List[str]] = None) -> List[str]:
    """Extract education degree titles from text using regex patterns.

    Args:
        text: Input text string.
        patterns: Optional list of regex patterns (defaults to EDUCATION_PATTERNS).

    Returns:
        List of normalized unique education degree titles.
    """
    if not isinstance(text, str) or not text:
        return []

    if patterns is None:
        patterns = EDUCATION_PATTERNS

    education = []
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            match = match.strip()
            if match and match.lower() not in [item.lower() for item in education]:
                education.append(match)

    return normalize_education(education)
