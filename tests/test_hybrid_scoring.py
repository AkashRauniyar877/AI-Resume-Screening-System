"""Validation test for hybrid scoring calculation and min-max normalization.

Validates weighted component scoring (skill 35%, semantic 30%, TF-IDF 20%, experience 15%),
min-max normalization, edge cases (identical scores, empty arrays), single vs batch
candidate normalization, and end-to-end pipeline hybrid score calculations.
"""

from pathlib import Path
import numpy as np
import pytest

from ai_engine.parser.pdf_parser import extract_text_from_pdf
from ai_engine.scoreing.skill_score import calculate_skill_score
from ai_engine.scoreing.experience_score import calculate_experience_score
from ai_engine.scoreing.overall_score import (
    min_max_normalize,
    calculate_hybrid_score,
    compute_batch_hybrid_scores,
)
from ai_engine.pipeline import process_resume, process_and_rank_candidates
from ai_engine.models import MatchingResult

JOB_DESCRIPTION_TEXT = """Full Stack Developer: Python, JavaScript, React, Node.js, Express, MongoDB, SQL, REST API, Git, GitHub, HTML, CSS, Data Structures and Algorithms."""

FILES = {
    "AJAY Chaudhary_resume.pdf": Path(r"C:\Users\Dell\Downloads\AJAY Chaudhary_resume.pdf"),
    "AJAY Chauhan_resume.pdf": Path(r"C:\Users\Dell\Downloads\AJAY Chauhan_resume.pdf"),
    "Resume.pdf": Path(r"C:\Users\Dell\Downloads\Resume.pdf"),
    "Akash_Shukla_Professional_Resume(20260924-090706).pdf": Path(
        r"C:\Users\Dell\OneDrive\Desktop\Akash_Shukla_Professional_Resume(20260924-090706).pdf"
    ),
}


def test_01_component_scores():
    """Test component skill and experience score functions."""

    # Skill score calculation
    cand_skills = ["python", "javascript", "react"]
    req_skills = ["python", "javascript", "react", "sql"]
    skill_score = calculate_skill_score(cand_skills, req_skills)
    assert skill_score == 75.0

    # Experience score calculation
    exp1 = calculate_experience_score(candidate_experience=5.0, required_experience=3.0)
    assert exp1 == 100.0  # Capped at 100%

    exp2 = calculate_experience_score(candidate_experience=1.5, required_experience=3.0)
    assert exp2 == 50.0

    exp3 = calculate_experience_score(candidate_experience=3.0, required_experience=0.0)
    assert exp3 == 0.0


def test_02_min_max_normalization():
    """Test min-max normalization behavior for standard and edge cases."""

    # Standard min-max normalization
    raw_scores = np.array([10.0, 20.0, 30.0, 40.0])
    norm_scores = min_max_normalize(raw_scores)
    assert abs(norm_scores[0] - 0.0) < 1e-5
    assert abs(norm_scores[1] - 33.333333) < 1e-4
    assert abs(norm_scores[2] - 66.666667) < 1e-4
    assert abs(norm_scores[3] - 100.0) < 1e-5

    # Edge case: Max == Min (identical scores)
    identical_scores = np.array([50.0, 50.0, 50.0])
    norm_identical = min_max_normalize(identical_scores)
    np.testing.assert_array_equal(norm_identical, np.array([50.0, 50.0, 50.0]))

    # Edge case: Empty input array
    empty_norm = min_max_normalize(np.array([]))
    assert len(empty_norm) == 0


def test_03_controlled_hybrid_scoring_cases():
    """Test controlled hybrid scoring cases (Cases 1-7)."""

    # Case 1: All 100% -> 100.0
    c1 = calculate_hybrid_score(100.0, 100.0, 100.0, 100.0)
    assert c1 == 100.0

    # Case 2: All 0% -> 0.0
    c2 = calculate_hybrid_score(0.0, 0.0, 0.0, 0.0)
    assert c2 == 0.0

    # Case 3: Skill = 100%, others = 0% -> 35.0 (35% weight)
    c3 = calculate_hybrid_score(100.0, 0.0, 0.0, 0.0)
    assert c3 == 35.0

    # Case 4: Semantic = 100%, others = 0% -> 30.0 (30% weight)
    c4 = calculate_hybrid_score(0.0, 100.0, 0.0, 0.0)
    assert c4 == 30.0

    # Case 5: TF-IDF = 100%, others = 0% -> 20.0 (20% weight)
    c5 = calculate_hybrid_score(0.0, 0.0, 100.0, 0.0)
    assert c5 == 20.0

    # Case 6: Experience = 100%, others = 0% -> 15.0 (15% weight)
    c6 = calculate_hybrid_score(0.0, 0.0, 0.0, 100.0)
    assert c6 == 15.0

    # Case 7: Component scores (80, 70, 60, 50)
    # Manual calculation: 0.35*80 + 0.30*70 + 0.20*60 + 0.15*50 = 28 + 21 + 12 + 7.5 = 68.5
    c7 = calculate_hybrid_score(80.0, 70.0, 60.0, 50.0)
    assert c7 == 68.5


def test_04_batch_vs_single_candidate_normalization():
    """Demonstrate how batch normalization alters relative hybrid scores."""

    single_path = FILES["AJAY Chaudhary_resume.pdf"]
    if not single_path.exists():
        pytest.skip(f"File not found: {single_path}")

    # Process single candidate
    single_res = process_resume(str(single_path), JOB_DESCRIPTION_TEXT)
    m_single = single_res.matching_result

    # Process batch of 4 candidates
    resumes = [{"path": str(p), "id": name} for name, p in FILES.items() if p.exists()]
    batch_res = process_and_rank_candidates(resumes, JOB_DESCRIPTION_TEXT)

    # Find AJAY Chaudhary in batch results
    ajay_batch = next(r for r in batch_res if r.candidate_id == "AJAY Chaudhary_resume.pdf")
    m_batch = ajay_batch.matching_result

    print("\n" + "=" * 80)
    print("SINGLE CANDIDATE VS BATCH NORMALIZATION DEMONSTRATION:")
    print(f"Single Candidate Hybrid Score: {m_single.hybrid_score:.2f}%")
    print(f"Batch Candidate Hybrid Score:  {m_batch.hybrid_score:.2f}%")
    print("=" * 80)

    # Verify single candidate uses clipped raw scores as fallback normalization
    assert m_single.semantic_normalized == m_single.semantic_score
    assert m_single.tfidf_normalized == m_single.tfidf_score

    # Verify batch candidate uses min-max normalized scores relative to batch
    assert m_batch.tfidf_normalized == 100.0  # AJAY Chaudhary has highest TF-IDF in batch


if __name__ == "__main__":
    test_01_component_scores()
    test_02_min_max_normalization()
    test_03_controlled_hybrid_scoring_cases()
    test_04_batch_vs_single_candidate_normalization()
