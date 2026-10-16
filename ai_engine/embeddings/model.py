"""Sentence Transformer model manager.

Provides lazy-loaded singleton instance of SentenceTransformer model.
"""

from typing import Optional
from sentence_transformers import SentenceTransformer
from ..config.ai_config import SEMANTIC_MODEL_NAME

_MODEL_INSTANCE: Optional[SentenceTransformer] = None


def get_semantic_model(model_name: str = SEMANTIC_MODEL_NAME) -> SentenceTransformer:
    """Get lazy-loaded singleton instance of SentenceTransformer model.

    Args:
        model_name: Name of sentence-transformer model (default: all-MiniLM-L6-v2).

    Returns:
        Loaded SentenceTransformer instance.
    """
    global _MODEL_INSTANCE
    if _MODEL_INSTANCE is None:
        _MODEL_INSTANCE = SentenceTransformer(model_name)
    return _MODEL_INSTANCE
