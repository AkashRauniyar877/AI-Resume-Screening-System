# AI Screening & Scoring Pipeline

The **AI Engine** (`ai_engine/`) processes uploaded candidate resumes and evaluates them against recruiter Job Descriptions (JD) through a multi-stage NLP and machine learning pipeline.

---

## AI Pipeline Flow

```
Job Description
      ↓
JD Analysis & Skill Extraction
      ↓
Resume PDF/DOCX Upload
      ↓
Text Parsing (PyMuPDF / python-docx)
      ↓
Text Preprocessing & Cleaning
      ↓
Entity & Skill Extraction
      ↓
TF-IDF Vector Match (Cosine Similarity)
      ↓
Semantic Vector Match (SentenceTransformers)
      ↓
Skill Coverage Calculation
      ↓
Experience Score Calculation
      ↓
Hybrid Composite Scoring
      ↓
Candidate Ranking
```

---

## Pipeline Stages

### 1. Resume Parsing & Text Extraction
- Converts PDF documents into plain text using `PyMuPDF` (`fitz`).
- Converts DOCX documents using `python-docx`.
- Falls back to UTF-8 plain text parsing.

### 2. Preprocessing & Normalization
- Removes headers, footers, special non-ASCII characters, and formatting noise.
- Normalizes whitespace and standardizes technical terminology.

### 3. Entity & Information Extraction
- **Candidate Name & Contact**: Extracted via structured regex patterns and NLP entity recognition.
- **Skills Extraction**: Matches extracted tokens against curated technical skill taxonomies.
- **Education Extraction**: Identifies degree levels (Bachelor's, Master's, PhD) and field keywords.
- **Experience Calculation**: Identifies employment date ranges and calculates total experience in years.

### 4. Match Algorithms

#### A. Skill Match & Coverage
- Computes matched skills, missing skills, and skill coverage ratio:
  $$\text{skill\_coverage} = \frac{|\text{Matched Skills}|}{|\text{Required Skills}|}$$

#### B. TF-IDF Similarity
- Vectorizes job description text and candidate resume text using `TfidfVectorizer` (`ngram_range=(1,2)`).
- Calculates cosine similarity between sparse vector representations.

#### C. Semantic Similarity
- Generates 384-dimensional dense contextual embeddings using the `all-MiniLM-L6-v2` transformer model.
- Calculates cosine similarity between JD embedding and resume text embedding to capture semantic context beyond literal keyword overlap.

#### D. Experience Scoring
- Compares candidate experience years ($E_{\text{cand}}$) against job description required experience ($E_{\text{req}}$):
  $$\text{experience\_score} = \min\left(1.0, \frac{E_{\text{cand}}}{\max(1.0, E_{\text{req}})}\right)$$

---

## Hybrid Composite Scoring Formula

The candidate's overall **Hybrid Score** (0–100 scale) is calculated using the following experimental weights:

$$\text{Hybrid Score} = \Big( 0.35 \times \text{skill\_coverage} + 0.30 \times \text{semantic\_normalized} + 0.20 \times \text{tfidf\_normalized} + 0.15 \times \text{experience\_score} \Big) \times 100$$

> **Note**: These scoring weights are project-specific experimental parameters configured in `ai_engine/scoreing/hybrid_scorer.py` and are subject to tuning during evaluation.
