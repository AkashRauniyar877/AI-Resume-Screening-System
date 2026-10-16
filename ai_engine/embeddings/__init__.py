"""Embeddings package initialization."""

from .model import get_semantic_model
from .generate_embeddings import generate_sentence_embeddings, generate_tfidf_matrix

__all__ = [
    "get_semantic_model",
    "generate_sentence_embeddings",
    "generate_tfidf_matrix",
]
