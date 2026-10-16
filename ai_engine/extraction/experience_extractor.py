"""Experience extraction module.

Uses explicit regex expressions to extract years of experience.
Unreliable date-range extraction is explicitly avoided.
"""

import re


def extract_experience(text: str) -> float:
    """Extract candidate total years of experience using explicit regex patterns.

    Per prompt requirements & Notebook findings:
    Uses explicit experience expressions such as '3 years of experience', '3+ years experience', '3 years in'.
    Does NOT use date-range extraction as the main experience extractor.
    Returns 0.0 if experience cannot be confidently extracted.

    Args:
        text: Input resume or job description text string.

    Returns:
        Extracted years of experience as float, defaulting to 0.0.
    """
    if not isinstance(text, str) or not text:
        return 0.0

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:yrs|years?)\s*(?:of\s*)?(?:professional\s*|relevant\s*|work\s*)?experience",
        r"(\d+(?:\.\d+)?)\+?\s*(?:yrs|years?)\s+in\s+",
        r"experience(?::|\s+of)?\s*(\d+(?:\.\d+)?)\+?\s*(?:yrs|years?)",
        r"(\d+(?:\.\d+)?)\+?\s*(?:yrs|years?)\s+working",
    ]

    experiences = []
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            try:
                val = float(match)
                if 0.0 <= val <= 60.0:  # Reasonable sanity check on extracted number
                    experiences.append(val)
            except ValueError:
                pass

    if experiences:
        return max(experiences)

    return 0.0
