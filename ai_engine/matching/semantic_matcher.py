"""Semantic matching module using Sentence Transformers.

Implements dense embedding cosine similarity matching Notebook 07.
"""

from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ..embeddings.model import get_semantic_model


def compute_semantic_similarity(
    job_description: str, resume_texts: List[str]
) -> np.ndarray:
    """Compute semantic cosine similarity percentage using all-MiniLM-L6-v2.

    Matches Notebook 07 methodology.

    Args:
        job_description: Job description text.
        resume_texts: List of processed resume texts.

    Returns:
        Numpy array of semantic score percentages (cosine_similarity * 100).
    """
    if not resume_texts:
        return np.array([])

    model = get_semantic_model()

    # Encode job description and resumes
    job_embedding = model.encode([job_description], show_progress_bar=False)
    resume_embeddings = model.encode(resume_texts, show_progress_bar=False)

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(job_embedding, resume_embeddings)
    scores = similarity_matrix[0]

    # Convert to percentage matching Notebook 07
    return scores * 100.0
