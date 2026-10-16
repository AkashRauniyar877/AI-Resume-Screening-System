"""Embedding generation module for semantic embeddings and TF-IDF vectors."""

from typing import List, Tuple, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from .model import get_semantic_model


def generate_sentence_embeddings(texts: List[str]) -> np.ndarray:
    """Generate 384-dimensional sentence transformer embeddings.

    Args:
        texts: List of text strings.

    Returns:
        Numpy array of shape (N, 384) representing dense embeddings.
    """
    if not texts:
        return np.empty((0, 384))

    model = get_semantic_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    return np.array(embeddings)


def generate_tfidf_matrix(
    corpus: List[str],
) -> Tuple[TfidfVectorizer, Any]:
    """Fit TfidfVectorizer on text corpus matching Notebook 03 default configuration.

    Args:
        corpus: List of preprocessed text strings.

    Returns:
        Tuple of (fitted TfidfVectorizer, tfidf_matrix).
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return vectorizer, tfidf_matrix
