"""Text cleaning module for raw resume and job description text."""

import re


def clean_raw_text(text: str) -> str:
    """Clean raw input text by lowercasing, stripping HTML tags, and normalizing whitespace.

    Args:
        text: Raw input text string.

    Returns:
        Cleaned text string.
    """
    if not isinstance(text, str) or not text:
        return ""

    # Convert to lowercase
    cleaned = text.lower()

    # Remove HTML tags (matching Resume_html cleaning in Notebook 01)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)

    # Replace multiple whitespace/newlines with a single space
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
