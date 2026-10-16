from pathlib import Path

from ai_engine.parser.pdf_parser import extract_text_from_pdf
from ai_engine.extraction.skill_extractor import extract_skills


FILES = [
    Path(r"C:\Users\Dell\Downloads\AJAY Chaudhary_resume.pdf"),
    Path(r"C:\Users\Dell\Downloads\AJAY Chauhan_resume.pdf"),
    Path(r"C:\Users\Dell\Downloads\Resume.pdf"),
    Path(r"C:\Users\Dell\OneDrive\Desktop\Akash_Shukla_Professional_Resume(20260924-090706).pdf"),
]


for file_path in FILES:
    print("\n" + "=" * 70)
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    text = extract_text_from_pdf(file_path)

    skills = extract_skills(text)

    print("\nEXTRACTED SKILLS:")

    for skill in skills:
        print("-", skill)