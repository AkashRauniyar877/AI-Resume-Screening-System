"""Validation test for Sentence Transformer semantic matching.

Validates dense embedding generation (all-MiniLM-L6-v2), vector dimensions (384),
cosine similarity calculations, model caching, boundary cases, and semantic similarity
between a real Full Stack Developer JD and 4 real candidate resumes.
"""

from pathlib import Path
import numpy as np
import pytest

from ai_engine.parser.pdf_parser import extract_text_from_pdf
from ai_engine.embeddings.model import get_semantic_model
from ai_engine.embeddings.generate_embeddings import generate_sentence_embeddings
from ai_engine.matching.semantic_matcher import compute_semantic_similarity

JOB_DESCRIPTION_TEXT = """Full Stack Developer

We are looking for a Full Stack Developer with experience in:
Python, JavaScript, React, Node.js, Express, MongoDB, SQL,
REST API, Git, GitHub, HTML, CSS and Data Structures and Algorithms.

Required skills:
Python
JavaScript
React
Node.js
Express
MongoDB
SQL
REST API
Git
GitHub
HTML
CSS
Data Structures and Algorithms"""

FILES = {
    "AJAY Chaudhary_resume.pdf": Path(r"C:\Users\Dell\Downloads\AJAY Chaudhary_resume.pdf"),
    "AJAY Chauhan_resume.pdf": Path(r"C:\Users\Dell\Downloads\AJAY Chauhan_resume.pdf"),
    "Resume.pdf": Path(r"C:\Users\Dell\Downloads\Resume.pdf"),
    "Akash_Shukla_Professional_Resume(20260924-090706).pdf": Path(
        r"C:\Users\Dell\OneDrive\Desktop\Akash_Shukla_Professional_Resume(20260924-090706).pdf"
    ),
}


def test_01_synthetic_semantic_pairs():
    """Test semantic similarity calculations on synthetic text pairs."""

    # TEST 1: High semantic similarity (Python/FastAPI developer)
    t1_a = "We need a developer who builds web applications using Python and FastAPI."
    t1_b = "Experienced in developing backend web applications with Python and FastAPI."
    sim1 = compute_semantic_similarity(t1_a, [t1_b])[0]

    # TEST 2: Low semantic similarity (Python developer vs Graphic Designer)
    t2_a = "We need a developer who builds web applications using Python and FastAPI."
    t2_b = "Experienced in graphic design, illustration, typography and visual branding."
    sim2 = compute_semantic_similarity(t2_a, [t2_b])[0]

    # TEST 3: High semantic similarity (REST API backend)
    t3_a = "Develop REST APIs and backend services."
    t3_b = "Build server-side APIs and backend applications."
    sim3 = compute_semantic_similarity(t3_a, [t3_b])[0]

    # TEST 4: Low semantic similarity (Backend dev vs Mechanical engineer)
    t4_a = "Python backend developer with FastAPI and MongoDB experience."
    t4_b = "Mechanical engineer experienced in AutoCAD, thermodynamics and manufacturing."
    sim4 = compute_semantic_similarity(t4_a, [t4_b])[0]

    print("\n" + "=" * 80)
    print("SYNTHETIC SEMANTIC SIMILARITY TESTS:")
    print(f"TEST 1 (Python dev vs Python dev): {sim1:.2f}% (raw float: {sim1/100:.4f})")
    print(f"TEST 2 (Python dev vs Graphic designer): {sim2:.2f}% (raw float: {sim2/100:.4f})")
    print(f"TEST 3 (REST API vs Server-side API): {sim3:.2f}% (raw float: {sim3/100:.4f})")
    print(f"TEST 4 (Backend dev vs Mechanical eng): {sim4:.2f}% (raw float: {sim4/100:.4f})")
    print("=" * 80)

    # Assert expected relative order and magnitude
    assert sim1 > 80.0, f"Expected >80% similarity for Test 1, got {sim1:.2f}%"
    assert sim2 < 30.0, f"Expected <30% similarity for Test 2, got {sim2:.2f}%"
    assert sim3 > 75.0, f"Expected >75% similarity for Test 3, got {sim3:.2f}%"
    assert sim4 < 25.0, f"Expected <25% similarity for Test 4, got {sim4:.2f}%"
    assert sim1 > sim2
    assert sim3 > sim4


def test_02_semantic_properties_and_boundaries():
    """Test model caching, embedding dimensions, same-text and empty-text handling."""

    # Model reuse / caching
    m1 = get_semantic_model()
    m2 = get_semantic_model()
    assert m1 is m2, "Model instance must be cached and reused as singleton"

    # Embedding dimension
    emb = generate_sentence_embeddings(["Sample text string"])
    assert isinstance(emb, np.ndarray)
    assert emb.shape == (1, 384), f"Expected shape (1, 384), got {emb.shape}"
    assert emb.shape[1] == 384, f"Expected dimension 384, got {emb.shape[1]}"

    # Same text vs same text similarity (~100%)
    text = "Full Stack Python JavaScript Developer"
    same_sim = compute_semantic_similarity(text, [text])[0]
    assert abs(same_sim - 100.0) < 0.01, f"Expected 100.0% for same text, got {same_sim}%"

    # Empty text list handling
    empty_res = compute_semantic_similarity(text, [])
    assert isinstance(empty_res, np.ndarray)
    assert len(empty_res) == 0, f"Expected empty array for empty list, got {empty_res}"

    empty_emb = generate_sentence_embeddings([])
    assert empty_emb.shape == (0, 384)


def test_03_real_resumes_semantic_matching():
    """Test semantic matching of 4 real PDF resumes against the Full Stack Developer JD."""

    jd_emb = generate_sentence_embeddings([JOB_DESCRIPTION_TEXT])
    assert jd_emb.shape == (1, 384)

    print("\n" + "=" * 80)
    print("REAL RESUMES SEMANTIC MATCHING (all-MiniLM-L6-v2):")
    print("=" * 80)

    for filename, file_path in FILES.items():
        if not file_path.exists():
            pytest.skip(f"File not found: {file_path}")

        resume_text = extract_text_from_pdf(file_path)
        assert len(resume_text) > 0, f"Resume text for {filename} is empty"

        res_emb = generate_sentence_embeddings([resume_text])
        sim_percentage = compute_semantic_similarity(JOB_DESCRIPTION_TEXT, [resume_text])[0]

        print(f"\nResume: {filename}")
        print(f"Semantic similarity: {sim_percentage:.2f}% (raw float: {sim_percentage/100:.4f})")
        print(f"Embedding shape: {res_emb.shape}")
        print(f"Embedding dimension: {res_emb.shape[1]}")

        assert res_emb.shape == (1, 384)
        assert res_emb.shape[1] == 384
        assert 0.0 <= sim_percentage <= 100.0


if __name__ == "__main__":
    test_01_synthetic_semantic_pairs()
    test_02_semantic_properties_and_boundaries()
    test_03_real_resumes_semantic_matching()
