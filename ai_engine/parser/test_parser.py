from ai_engine.parser.text_extractor import extract_text


file_path = "data/resumes/data/accountant/10554236.pdf"

text = extract_text(file_path)

print("Extracted text:")
print(text[:2000])