"""Parser package initialization."""

from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx
from .text_extractor import extract_text

__all__ = [
    "extract_text_from_pdf",
    "extract_text_from_docx",
    "extract_text",
]
