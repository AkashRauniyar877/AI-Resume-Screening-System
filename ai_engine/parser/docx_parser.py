"""DOCX text extractor using python-docx."""

import os
from docx import Document


def extract_text_from_docx(file_path: str) -> str:
    """Extract raw text from a DOCX file.

    Args:
        file_path: Path to the DOCX file.

    Returns:
        Extracted text content as string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    return "\n".join(paragraphs)