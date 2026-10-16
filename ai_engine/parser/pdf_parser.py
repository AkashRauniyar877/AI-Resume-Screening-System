"""PDF text extractor using PyMuPDF (pymupdf)."""

import os
import pymupdf


def extract_text_from_pdf(file_path: str) -> str:
    """Extract raw text from a PDF file using pymupdf.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text content as string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text_content = []
    doc = pymupdf.open(file_path)
    try:
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text_content.append(page_text)
    finally:
        doc.close()

    return "\n".join(text_content)