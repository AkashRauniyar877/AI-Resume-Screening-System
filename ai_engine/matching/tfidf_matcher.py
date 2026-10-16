"""TF-IDF matching module.

Implements TF-IDF vectorization and cosine similarity matching Notebook 03.
"""

from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_tfidf_similarity(
    job_description: str, processed_resumes: List[str]
) -> np.ndarray:
    """Compute TF-IDF cosine similarity scores between job description and resumes.

    Matches Notebook 03 methodology.

    Args:
        job_description: Job description text (processed or raw).
        processed_resumes: List of preprocessed resume texts.

    Returns:
        Numpy array of similarity percentage scores (0..100).
    """
    if not processed_resumes:
        return np.array([])

    vectorizer = TfidfVectorizer()

    # Fit vectorizer on resume corpus
    tfidf_matrix = vectorizer.fit_transform(processed_resumes)

    # Transform job description vector
    job_vector = vectorizer.transform([job_description])

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(job_vector, tfidf_matrix)
    scores = similarity_matrix[0]

    # Convert to percentage matching Notebook 03
    return scores * 100.0
