"""General similarity measurement utilities."""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between two feature matrix representations."""
    return cosine_similarity(vec1, vec2)
