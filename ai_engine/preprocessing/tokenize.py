"""Tokenization and stop-word filtering module.

Replicates the NLP preprocessing pipeline from Notebook 02 using NLTK.
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from .clean_text import clean_raw_text

# Ensure necessary NLTK data files are downloaded silently
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

try:
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    STOP_WORDS = set()


def preprocess_text(text: str) -> str:
    """Preprocess text using NLTK tokenization and English stop word filtering.

    Matches Notebook 02 preprocessing logic.

    Args:
        text: Raw or cleaned text string.

    Returns:
        Space-separated string of filtered tokens.
    """
    cleaned = clean_raw_text(text)
    if not cleaned:
        return ""

    try:
        tokens = word_tokenize(cleaned)
    except Exception:
        tokens = cleaned.split()

    filtered_tokens = [word for word in tokens if word not in STOP_WORDS]
    return " ".join(filtered_tokens)
