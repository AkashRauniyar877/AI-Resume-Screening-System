"""Validation test for TF-IDF vectorization and cosine similarity matching.

Validates TfidfVectorizer configuration, single/batch vector transformations,
cosine similarity calculations, boundary conditions, and TF-IDF similarity between
a real Full Stack Developer JD and 4 real candidate resumes.
"""

from pathlib import Path
import numpy as np
import pytest

from ai_engine.parser.pdf_parser import extract_text_from_pdf
from ai_engine.preprocessing import preprocess_text
from ai_engine.matching.tfidf_matcher import compute_tfidf_similarity
from ai_engine.embeddings.generate_embeddings import generate_tfidf_matrix
from ai_engine.scoreing.overall_score import min_max_normalize

JOB_DESCRIPTION_TEXT = """Full Stack Developer: Python, JavaScript, React, Node.js, Express, MongoDB, SQL, REST API, Git, GitHub, HTML, CSS, Data Structures and Algorithms."""

FILES = {
    "AJAY Chaudhary_resume.pdf": Path(r"C:\Users\Dell\Downloads\AJAY Chaudhary_resume.pdf"),
    "AJAY Chauhan_resume.pdf": Path(r"C:\Users\Dell\Downloads\AJAY Chauhan_resume.pdf"),
    "Resume.pdf": Path(r"C:\Users\Dell\Downloads\Resume.pdf"),
    "Akash_Shukla_Professional_Resume(20260924-090706).pdf": Path(
        r"C:\Users\Dell\OneDrive\Desktop\Akash_Shukla_Professional_Resume(20260924-090706).pdf"
    ),
}


def test_01_controlled_tfidf_cases():
    """Test TF-IDF similarity on controlled synthetic text pairs (TESTS 1-5)."""

    # TEST 1 — High lexical similarity
    t1_jd = preprocess_text("We need a Python developer with FastAPI and MongoDB experience.")
    t1_res = preprocess_text(
        "Experienced Python developer working with FastAPI applications and MongoDB databases."
    )
    sim1 = compute_tfidf_similarity(t1_jd, [t1_res])[0]

    # TEST 2 — Low lexical similarity
    t2_jd = preprocess_text("We need a Python developer with FastAPI and MongoDB experience.")
    t2_res = preprocess_text(
        "Experienced graphic designer specializing in illustration, typography and visual branding."
    )
    sim2 = compute_tfidf_similarity(t2_jd, [t2_res])[0]

    # TEST 3 — Exact same text
    t3_text = preprocess_text("We need a Python developer with FastAPI and MongoDB experience.")
    sim3 = compute_tfidf_similarity(t3_text, [t3_text])[0]

    # TEST 4 — Partial keyword overlap
    t4_jd = preprocess_text("Python FastAPI MongoDB React JavaScript")
    t4_res = preprocess_text("Python JavaScript HTML CSS")
    sim4 = compute_tfidf_similarity(t4_jd, [t4_res])[0]

    # TEST 5 — No meaningful overlap
    t5_jd = preprocess_text("Python FastAPI MongoDB React JavaScript")
    t5_res = preprocess_text("Mechanical engineering thermodynamics manufacturing AutoCAD")
    sim5 = compute_tfidf_similarity(t5_jd, [t5_res])[0]

    print("\n" + "=" * 80)
    print("CONTROLLED TF-IDF TESTS:")
    print(f"TEST 1 (High lexical similarity): {sim1:.2f}% (raw float: {sim1/100:.4f})")
    print(f"TEST 2 (Low lexical similarity):  {sim2:.2f}% (raw float: {sim2/100:.4f})")
    print(f"TEST 3 (Exact same text):        {sim3:.2f}% (raw float: {sim3/100:.4f})")
    print(f"TEST 4 (Partial keyword overlap): {sim4:.2f}% (raw float: {sim4/100:.4f})")
    print(f"TEST 5 (No overlap):             {sim5:.2f}% (raw float: {sim5/100:.4f})")
    print("=" * 80)

    # Assertions
    assert sim1 > 50.0, f"Expected >50% for Test 1, got {sim1:.2f}%"
    assert sim2 == 0.0, f"Expected 0% for Test 2, got {sim2:.2f}%"
    assert abs(sim3 - 100.0) < 0.01, f"Expected 100% for Test 3, got {sim3:.2f}%"
    assert sim4 > 50.0, f"Expected >50% for Test 4, got {sim4:.2f}%"
    assert sim5 == 0.0, f"Expected 0% for Test 5, got {sim5:.2f}%"


def test_02_tfidf_vectorizer_properties_and_boundaries():
    """Test TF-IDF helper function, boundary cases, and independent batch processing."""

    # Empty resume list input behavior
    empty_sims = compute_tfidf_similarity("python developer", [])
    assert isinstance(empty_sims, np.ndarray)
    assert len(empty_sims) == 0

    # Verify generate_tfidf_matrix helper from embeddings module
    corpus = [preprocess_text("Python developer"), preprocess_text("Java developer")]
    vectorizer, matrix = generate_tfidf_matrix(corpus)
    assert matrix.shape == (2, 3)
    assert vectorizer.ngram_range == (1, 1)

    # Multiple resumes processed independently
    jd = preprocess_text("Python FastAPI backend developer")
    res1 = preprocess_text("Python backend engineer")
    res2 = preprocess_text("Java frontend developer")
    res_batch = [res1, res2]
    sims = compute_tfidf_similarity(jd, res_batch)
    assert len(sims) == 2
    assert sims[0] > sims[1]


def test_03_real_resumes_tfidf_matching():
    """Test TF-IDF matching on 4 real PDF resumes against Full Stack Developer JD."""

    p_jd = preprocess_text(JOB_DESCRIPTION_TEXT)
    res_texts = []
    res_names = []

    for filename, file_path in FILES.items():
        if not file_path.exists():
            pytest.skip(f"File not found: {file_path}")

        raw_text = extract_text_from_pdf(file_path)
        p_text = preprocess_text(raw_text)
        res_texts.append(p_text)
        res_names.append(filename)

    batch_sims = compute_tfidf_similarity(p_jd, res_texts)
    norm_sims = min_max_normalize(batch_sims)

    print("\n" + "=" * 80)
    print("REAL RESUMES TF-IDF MATCHING:")
    print("=" * 80)

    for i, name in enumerate(res_names):
        raw_pct = batch_sims[i]
        raw_flt = raw_pct / 100.0
        norm_val = norm_sims[i]

        print(f"\nResume: {name}")
        print(f"  TF-IDF similarity: {raw_pct:.2f}%")
        print(f"  Raw similarity float (0..1): {raw_flt:.4f}")
        print(f"  Min-Max Normalized score (0..100): {norm_val:.2f}%")

        assert 0.0 <= raw_pct <= 100.0
        assert 0.0 <= raw_flt <= 1.0
        assert 0.0 <= norm_val <= 100.0


if __name__ == "__main__":
    test_01_controlled_tfidf_cases()
    test_02_tfidf_vectorizer_properties_and_boundaries()
    test_03_real_resumes_tfidf_matching()
