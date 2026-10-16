"""Contact information extraction module (email and phone).

Implements regex extractors matching Notebook 09 logic.
"""

import re
from typing import Optional


def extract_email(text: str) -> Optional[str]:
    """Extract candidate email address using regex pattern matching.

    Args:
        text: Resume raw text.

    Returns:
        Extracted email address as string or None if not found.
    """
    if not isinstance(text, str) or not text:
        return None

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    match = re.search(pattern, text)
    if match:
        return match.group()
    return None


def extract_phone(text: str) -> Optional[str]:
    """Extract candidate phone number using regex pattern matching.

    Args:
        text: Resume raw text.

    Returns:
        Extracted phone number as string or None if not found.
    """
    if not isinstance(text, str) or not text:
        return None

    pattern = r"(?<!\d)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}(?!\d)"
    match = re.search(pattern, text)
    if match:
        return match.group()
    return None
