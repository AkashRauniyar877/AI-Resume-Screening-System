import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from ai_engine.parser.pdf_parser import extract_text_from_pdf
from ai_engine.extraction.skill_extractor import extract_skills


FILES = {
    "AJAY Chaudhary_resume.pdf":
        Path(r"C:\Users\Dell\Downloads\AJAY Chaudhary_resume.pdf"),

    "AJAY Chauhan_resume.pdf":
        Path(r"C:\Users\Dell\Downloads\AJAY Chauhan_resume.pdf"),

    "Resume.pdf":
        Path(r"C:\Users\Dell\Downloads\Resume.pdf"),

    "Akash_Shukla_Professional_Resume(20260924-090706).pdf":
        Path(
            r"C:\Users\Dell\OneDrive\Desktop\Akash_Shukla_Professional_Resume(20260924-090706).pdf"
        ),
}


EXPECTED_SKILLS = {
    "AJAY Chaudhary_resume.pdf": [
        "c++",
        "java",
        "python",
        "javascript",
        "html",
        "css",
        "react",
        "node.js",
        "express",
        "mongodb",
        "git",
        "github",
        "vs code",
        "data structures and algorithms",
        "object oriented programming",
    ],

    "AJAY Chauhan_resume.pdf": [
        "python",
        "data structures and algorithms",
        "machine learning",
        "numpy",
        "pandas",
        "scikit-learn",
        "git",
        "github",
        "vs code",
        "data analysis",
    ],

    "Resume.pdf": [
        "c",
        "python",
        "java",
        "html",
        "css",
        "javascript",
        "vs code",
        "git",
        "github",
    ],

    "Akash_Shukla_Professional_Resume(20260924-090706).pdf": [
        "c++",
        "java",
        "python",
        "javascript",
        "sql",
        "html",
        "css",
        "rest api",
        "fastapi",
        "jdbc",
        "gemini api",
        "easyocr",
        "apscheduler",
        "git",
        "github",
        "vs code",
        "mysql",
        "dbms",
        "object oriented programming",
        "operating systems",
        "computer networks",
    ],
}


for filename, expected in EXPECTED_SKILLS.items():

    file_path = FILES[filename]

    if not file_path.exists():
        print(f"\nFILE NOT FOUND: {file_path}")
        continue

    text = extract_text_from_pdf(file_path)

    extracted = set(extract_skills(text))
    expected_set = set(expected)

    missing = expected_set - extracted
    found = expected_set & extracted

    print("\n" + "=" * 70)
    print(filename)
    print("=" * 70)

    print("\nFOUND:")
    for skill in sorted(found):
        print("-", skill)

    print("\nMISSING:")
    if missing:
        for skill in sorted(missing):
            print("-", skill)
    else:
        print("None")

    coverage = (
        len(found) / len(expected_set) * 100
        if expected_set
        else 100
    )

    print(f"\nEXPECTED SKILL COVERAGE: {coverage:.2f}%")