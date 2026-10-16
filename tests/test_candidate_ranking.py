"""Validation test for candidate ranking logic.

Validates descending hybrid score sorting, 1-based rank assignment, tie score stability,
edge cases (empty lists, single candidate, identical scores), and real candidate ranking.
"""

from pathlib import Path
import pytest

from ai_engine.models import ResumeInformation, MatchingResult, CandidateRankingResult
from ai_engine.ranking.candidate_ranker import rank_candidates
from ai_engine.pipeline import process_and_rank_candidates

JOB_DESCRIPTION_TEXT = """Full Stack Developer: Python, JavaScript, React, Node.js, Express, MongoDB, SQL, REST API, Git, GitHub, HTML, CSS, Data Structures and Algorithms."""

FILES = {
    "AJAY Chaudhary_resume.pdf": Path(r"C:\Users\Dell\Downloads\AJAY Chaudhary_resume.pdf"),
    "AJAY Chauhan_resume.pdf": Path(r"C:\Users\Dell\Downloads\AJAY Chauhan_resume.pdf"),
    "Resume.pdf": Path(r"C:\Users\Dell\Downloads\Resume.pdf"),
    "Akash_Shukla_Professional_Resume(20260924-090706).pdf": Path(
        r"C:\Users\Dell\OneDrive\Desktop\Akash_Shukla_Professional_Resume(20260924-090706).pdf"
    ),
}


def _make_pair(candidate_id: str, score: float):
    info = ResumeInformation(id=candidate_id, name=f"Candidate {candidate_id}")
    match = MatchingResult(candidate_id=candidate_id, hybrid_score=score)
    return (info, match)


def test_01_controlled_ranking_cases():
    """Test controlled candidate ranking scenarios (TESTS 1-6)."""

    # TEST 1 — Basic descending ranking
    pairs1 = [_make_pair("A", 85.0), _make_pair("B", 72.0), _make_pair("C", 91.0), _make_pair("D", 60.0)]
    r1 = rank_candidates(pairs1)
    assert [item.candidate_id for item in r1] == ["C", "A", "B", "D"]
    assert [item.rank for item in r1] == [1, 2, 3, 4]

    # TEST 2 — Already sorted input
    pairs2 = [_make_pair("A", 95.0), _make_pair("B", 80.0), _make_pair("C", 70.0), _make_pair("D", 50.0)]
    r2 = rank_candidates(pairs2)
    assert [item.candidate_id for item in r2] == ["A", "B", "C", "D"]
    assert [item.rank for item in r2] == [1, 2, 3, 4]

    # TEST 3 — Reverse order input
    pairs3 = [_make_pair("A", 50.0), _make_pair("B", 70.0), _make_pair("C", 80.0), _make_pair("D", 95.0)]
    r3 = rank_candidates(pairs3)
    assert [item.candidate_id for item in r3] == ["D", "C", "B", "A"]
    assert [item.rank for item in r3] == [1, 2, 3, 4]

    # TEST 4 — Tie scores (Python stable sort preserves original insertion order)
    pairs4 = [_make_pair("A", 90.0), _make_pair("B", 90.0), _make_pair("C", 80.0), _make_pair("D", 70.0)]
    r4 = rank_candidates(pairs4)
    assert [item.candidate_id for item in r4] == ["A", "B", "C", "D"]
    assert [item.rank for item in r4] == [1, 2, 3, 4]

    # TEST 5 — Identical scores
    pairs5 = [_make_pair("A", 75.0), _make_pair("B", 75.0), _make_pair("C", 75.0), _make_pair("D", 75.0)]
    r5 = rank_candidates(pairs5)
    assert [item.candidate_id for item in r5] == ["A", "B", "C", "D"]
    assert [item.rank for item in r5] == [1, 2, 3, 4]

    # TEST 6 — Zero scores
    pairs6 = [_make_pair("A", 0.0), _make_pair("B", 40.0), _make_pair("C", 0.0), _make_pair("D", 80.0)]
    r6 = rank_candidates(pairs6)
    assert [item.candidate_id for item in r6] == ["D", "B", "A", "C"]
    assert [item.rank for item in r6] == [1, 2, 3, 4]


def test_02_edge_cases():
    """Test boundary cases for empty lists, single candidate, and 2 candidates."""

    # Empty candidate list
    assert rank_candidates([]) == []

    # Single candidate
    r_single = rank_candidates([_make_pair("A", 88.0)])
    assert len(r_single) == 1
    assert r_single[0].rank == 1
    assert r_single[0].candidate_id == "A"

    # Two candidates
    r_two = rank_candidates([_make_pair("A", 50.0), _make_pair("B", 75.0)])
    assert len(r_two) == 2
    assert r_two[0].candidate_id == "B"
    assert r_two[0].rank == 1
    assert r_two[1].candidate_id == "A"
    assert r_two[1].rank == 2


def test_03_real_resumes_ranking():
    """Test ranking of 4 real resumes against the Full Stack Developer JD."""

    resumes = [{"path": str(p), "id": name} for name, p in FILES.items() if p.exists()]
    if len(resumes) < 4:
        pytest.skip("Not all real resume PDF files are available")

    ranked = process_and_rank_candidates(resumes, JOB_DESCRIPTION_TEXT)
    assert len(ranked) == 4

    print("\n" + "=" * 80)
    print("REAL RESUMES RANKING RESULTS:")
    print("=" * 80)

    for item in ranked:
        m = item.matching_result
        print(f"\nRank {item.rank}: Candidate = {item.candidate_id}")
        print(f"  Skill Coverage:      {m.skill_coverage:.2f}%")
        print(f"  Semantic Score:      {m.semantic_score:.2f}% (Normalized: {m.semantic_normalized:.2f}%)")
        print(f"  TF-IDF Score:        {m.tfidf_score:.2f}% (Normalized: {m.tfidf_normalized:.2f}%)")
        print(f"  Experience Score:    {m.experience_score:.2f}%")
        print(f"  Final Hybrid Score:  {m.hybrid_score:.2f}%")

    # Verify scores are strictly monotonically non-increasing
    scores = [item.hybrid_score for item in ranked]
    ranks = [item.rank for item in ranked]

    assert ranks == [1, 2, 3, 4]
    assert scores == sorted(scores, reverse=True)


if __name__ == "__main__":
    test_01_controlled_ranking_cases()
    test_02_edge_cases()
    test_03_real_resumes_ranking()
