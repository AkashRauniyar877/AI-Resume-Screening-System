"""Text normalization utilities."""

import re


def normalize_whitespace(text: str) -> str:
    """Normalize repeated spaces and newlines into single spaces."""
    if not isinstance(text, str):
        return ""
    return re.sub(r"\s+", " ", text).strip()
