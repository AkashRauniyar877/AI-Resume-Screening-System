"""Validation test for real job description to real resume skill matching.

Validates extracting skills from a real JD, extracting skills from 4 real resumes,
and computing matched skills, missing skills, and skill coverage percentage.
"""

from pathlib import Path
import pytest
from ai_engine.parser.pdf_parser import extract_text_from_pdf
from ai_engine.extraction.skill_extractor import extract_skills
from ai_engine.matching.keyword_matcher import calculate_skill_match

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

EXPECTED_MATCH_SUMMARY = {
    "AJAY Chaudhary_resume.pdf": {
        "matched_count": 11,
        "missing_count": 2,
        "coverage_approx": 84.62,
    },
    "AJAY Chauhan_resume.pdf": {
        "matched_count": 4,
        "missing_count": 9,
        "coverage_approx": 30.77,
    },
    "Resume.pdf": {
        "matched_count": 8,
        "missing_count": 5,
        "coverage_approx": 61.54,
    },
    "Akash_Shukla_Professional_Resume(20260924-090706).pdf": {
        "matched_count": 8,
        "missing_count": 5,
        "coverage_approx": 61.54,
    },
}


def test_real_resume_skill_matching():
    """Extract skills from JD and real resumes and validate skill matching logic."""

    # 1. Extract required skills from Job Description
    jd_skills = extract_skills(JOB_DESCRIPTION_TEXT)
    expected_jd_skills = {
        "python",
        "javascript",
        "react",
        "node.js",
        "express",
        "mongodb",
        "sql",
        "rest api",
        "git",
        "github",
        "html",
        "css",
        "data structures and algorithms",
    }
    assert set(jd_skills) == expected_jd_skills, (
        f"Expected JD skills {expected_jd_skills}, got {set(jd_skills)}"
    )

    print("\n" + "=" * 80)
    print("REAL JOB DESCRIPTION SKILLS EXTRACTED:")
    print(sorted(jd_skills))
    print("=" * 80)

    # 2. Extract and match skills for each real resume
    for filename, file_path in FILES.items():
        if not file_path.exists():
            pytest.skip(f"File not found: {file_path}")

        resume_text = extract_text_from_pdf(file_path)
        resume_skills = extract_skills(resume_text)

        matched_skills, missing_skills, coverage = calculate_skill_match(
            candidate_skills=resume_skills, required_skills=jd_skills
        )

        print("\n----------------------------------------")
        print(f"Candidate/Resume: {filename}")
        print(f"JD Skills: {sorted(jd_skills)}")
        print(f"Resume Skills: {sorted(resume_skills)}")
        print(f"Matched Skills: {sorted(matched_skills)}")
        print(f"Missing Skills: {sorted(missing_skills)}")
        print(f"Skill Coverage: {coverage:.2f}%")

        expected = EXPECTED_MATCH_SUMMARY[filename]
        assert len(matched_skills) == expected["matched_count"]
        assert len(missing_skills) == expected["missing_count"]
        assert abs(coverage - expected["coverage_approx"]) < 0.1

        # 3. Verify obvious match boundary conditions
        # - Java != JavaScript
        if "java" in resume_skills and "javascript" not in resume_skills:
            assert "javascript" not in matched_skills
        # - SQL != MySQL (unless SQL itself is present)
        if "mysql" in resume_skills and "sql" not in resume_skills:
            assert "sql" not in matched_skills


if __name__ == "__main__":
    test_real_resume_skill_matching()
