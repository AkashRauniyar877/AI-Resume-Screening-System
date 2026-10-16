"""Text extractor interface supporting PDF, DOCX, plain text files, and raw string inputs."""

import os
from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx


def extract_text(file_path_or_text: str) -> str:
    """Extract raw text from PDF, DOCX, TXT file path or return raw text string directly.

    Args:
        file_path_or_text: File path or raw text string.

    Returns:
        Extracted or direct text string.
    """
    if not isinstance(file_path_or_text, str) or not file_path_or_text.strip():
        return ""

    # If it is an existing file path on disk
    if os.path.exists(file_path_or_text) and os.path.isfile(file_path_or_text):
        ext = os.path.splitext(file_path_or_text)[1].lower()
        if ext == ".pdf":
            return extract_text_from_pdf(file_path_or_text)
        elif ext == ".docx":
            return extract_text_from_docx(file_path_or_text)
        elif ext in [".txt", ".csv", ".json", ".md"]:
            with open(file_path_or_text, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            raise ValueError(
                f"Unsupported file extension '{ext}'. Only PDF, DOCX, and TXT are supported."
            )

    # If it's a raw text input (contains spaces, newlines, or is text content)
    if "\n" in file_path_or_text or " " in file_path_or_text or len(file_path_or_text) > 50:
        return file_path_or_text

    # If it looks like a missing file path
    raise FileNotFoundError(f"File not found: {file_path_or_text}")