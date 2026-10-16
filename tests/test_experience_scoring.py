"""Validation test for experience extraction and experience score calculation.

Validates explicit experience extraction regex patterns, phrase variations, edge cases,
date-range non-support by design, internship handling, and real candidate resume extraction.
"""

from pathlib import Path
import pytest

from ai_engine.parser.pdf_parser import extract_text_from_pdf
from ai_engine.extraction.experience_extractor import extract_experience
from ai_engine.scoreing.experience_score import calculate_experience_score

JOB_DESCRIPTION_TEXT = """Full Stack Developer: Python, JavaScript, React, Node.js, Express, MongoDB, SQL, REST API, Git, GitHub, HTML, CSS, Data Structures and Algorithms."""

FILES = {
    "AJAY Chaudhary_resume.pdf": Path(r"C:\Users\Dell\Downloads\AJAY Chaudhary_resume.pdf"),
    "AJAY Chauhan_resume.pdf": Path(r"C:\Users\Dell\Downloads\AJAY Chauhan_resume.pdf"),
    "Resume.pdf": Path(r"C:\Users\Dell\Downloads\Resume.pdf"),
    "Akash_Shukla_Professional_Resume(20260924-090706).pdf": Path(
        r"C:\Users\Dell\OneDrive\Desktop\Akash_Shukla_Professional_Resume(20260924-090706).pdf"
    ),
}


def test_01_explicit_experience():
    """Test explicit experience extraction and scoring (TEST 1)."""
    text = "Software Developer with 3 years of experience."
    exp = extract_experience(text)
    score = calculate_experience_score(candidate_experience=exp, required_experience=3.0)

    print("\nTEST 1 (Explicit Experience):")
    print(f"Extracted: {exp} years, Score vs 3.0 yrs required: {score:.2f}%")

    assert exp == 3.0
    assert score == 100.0


def test_02_different_experience_values():
    """Test various explicit numerical experience values (TEST 2)."""
    cases = [
        ("1 year of experience", 1.0, 33.33),
        ("2 years of experience", 2.0, 66.67),
        ("3 years of experience", 3.0, 100.00),
        ("5 years of experience", 5.0, 100.00),
        ("8 years of experience", 8.0, 100.00),
    ]

    print("\nTEST 2 (Different Experience Values vs 3.0 yrs required):")
    for phrase, expected_exp, expected_score_approx in cases:
        exp = extract_experience(phrase)
        score = calculate_experience_score(exp, required_experience=3.0)
        print(f"Phrase: '{phrase}' -> Extracted: {exp} yrs, Score: {score:.2f}%")
        assert exp == expected_exp
        assert abs(score - expected_score_approx) < 0.1


def test_03_experience_phrase_variations():
    """Test supported experience phrase variations (TEST 3)."""
    supported_phrases = [
        ("3+ years experience", 3.0),
        ("3 years of professional experience", 3.0),
        ("5 years professional experience", 5.0),
        ("4 years of relevant experience", 4.0),
        ("4 years of work experience", 4.0),
    ]

    print("\nTEST 3 (Experience Phrase Variations):")
    for phrase, expected_exp in supported_phrases:
        exp = extract_experience(phrase)
        print(f"Phrase: '{phrase}' -> Extracted: {exp} yrs")
        assert exp == expected_exp

    # Document phrases not supported by current single-modifier regex pattern
    unsupported_phrases = [
        "worked for 3 years as a software developer",
        "4 years of relevant work experience",  # multi-word modifier ('relevant work')
    ]
    for phrase in unsupported_phrases:
        exp = extract_experience(phrase)
        print(f"Phrase: '{phrase}' -> Extracted: {exp} yrs (Not matched by current production regex)")
        assert exp == 0.0


def test_04_no_experience():
    """Test text with no explicit experience statement (TEST 4)."""
    text = "Recent Computer Science graduate with skills in Python, React and MongoDB."
    exp = extract_experience(text)
    score = calculate_experience_score(exp, required_experience=3.0)

    print("\nTEST 4 (No Experience):")
    print(f"Extracted: {exp} yrs, Score: {score:.2f}%")

    assert exp == 0.0
    assert score == 0.0


def test_05_fresher():
    """Test fresher resume text (TEST 5)."""
    text = "Fresher with strong skills in Python and JavaScript."
    exp = extract_experience(text)
    score = calculate_experience_score(exp, required_experience=3.0)

    print("\nTEST 5 (Fresher):")
    print(f"Extracted: {exp} yrs, Score: {score:.2f}%")

    assert exp == 0.0
    assert score == 0.0


def test_06_internship():
    """Test internship experience statement (TEST 6)."""
    text = "Completed a 6 month software development internship."
    exp = extract_experience(text)
    score = calculate_experience_score(exp, required_experience=3.0)

    print("\nTEST 6 (Internship):")
    print(f"Extracted: {exp} yrs (Internship without 'years of experience' phrase defaults to 0.0)")

    assert exp == 0.0
    assert score == 0.0


def test_07_date_range():
    """Test date-range text format (TEST 7)."""
    text = "Software Developer, Jan 2022 - Dec 2024"
    exp = extract_experience(text)

    print("\nTEST 7 (Date Range):")
    print(f"Extracted: {exp} yrs (Date-range parsing is explicitly non-supported by design)")

    assert exp == 0.0


def test_08_real_resumes_experience():
    """Test experience extraction on the 4 real PDF resumes (TEST 8)."""

    print("\n" + "=" * 80)
    print("REAL RESUMES EXPERIENCE EXTRACTION & SCORING:")
    print("=" * 80)

    for filename, file_path in FILES.items():
        if not file_path.exists():
            pytest.skip(f"File not found: {file_path}")

        raw_text = extract_text_from_pdf(file_path)
        exp = extract_experience(raw_text)
        score_3yrs = calculate_experience_score(exp, required_experience=3.0)
        score_0yrs = calculate_experience_score(exp, required_experience=0.0)

        print(f"\nResume: {filename}")
        print(f"  Extracted Experience: {exp} years")
        print(f"  Experience Score (vs 3.0 yrs required): {score_3yrs:.2f}%")
        print(f"  Experience Score (vs 0.0 yrs required): {score_0yrs:.2f}%")
        print(f"  Explicit Experience Phrase Present: {'Yes' if exp > 0 else 'No (B.Tech student fresher)'}")

        assert exp == 0.0
        assert score_3yrs == 0.0
        assert score_0yrs == 0.0


def test_09_edge_cases():
    """Test boundary cases for empty text, None, and multiple experience statements."""

    # Empty text
    assert extract_experience("") == 0.0

    # None input
    assert extract_experience(None) == 0.0  # type: ignore

    # Text with no experience
    assert extract_experience("Python JavaScript developer") == 0.0

    # Multiple experience statements (returns max extracted value)
    multi_text = "2 years of experience in Python and 5 years of experience in Java."
    assert extract_experience(multi_text) == 5.0


if __name__ == "__main__":
    test_01_explicit_experience()
    test_02_different_experience_values()
    test_03_experience_phrase_variations()
    test_04_no_experience()
    test_05_fresher()
    test_06_internship()
    test_07_date_range()
    test_08_real_resumes_experience()
    test_09_edge_cases()
