# AI Resume Screening and Candidate Shortlisting System

An AI/NLP-assisted application designed to parse, screen, evaluate, and rank candidate resumes against Job Descriptions (JD) to accelerate initial recruiter shortlisting workflows.

> **Important Note**: This system is designed as an assistant for recruiters to perform initial candidate shortlisting. It is **not** intended to replace human recruiters or make automated hiring decisions.

---

## 1. Problem Statement

Modern talent acquisition teams frequently receive hundreds of resumes for a single job opening. Manually reading each resume, extracting relevant candidate qualifications, comparing them against job criteria, and shortlisting qualified candidates is time-consuming, repetitive, and prone to human fatigue and inconsistency.

---

## 2. Objective

The **AI Resume Screening System** provides an automated, objective, and scalable initial candidate screening framework:
- Parse multi-format resume documents (`PDF`, `DOCX`, `TXT`).
- Extract structured candidate metadata (Name, Email, Phone, Skills, Education, Experience).
- Analyze Job Descriptions to extract required skills, experience, and education benchmarks.
- Calculate matching scores using sparse TF-IDF vector similarity, dense transformer-based semantic embeddings, skill coverage ratios, and experience alignment.
- Compute a composite **Hybrid Score** and rank candidates in real-time.
- Persist structured candidate records, job metadata, and screening results in MongoDB under recruiter ownership.
- Provide a modern React dashboard with secure inline resume previewing and downloading.

---

## 3. AI Pipeline Overview

```
Job Description
      ↓
JD Analysis
      ↓
Resume Parsing
      ↓
Text Preprocessing
      ↓
Information Extraction
      ↓
Skill Matching
      ↓
TF-IDF Similarity
      ↓
Semantic Similarity
      ↓
Experience Scoring
      ↓
Hybrid Score
      ↓
Candidate Ranking
```

### Pipeline Stages
1. **JD Analysis**: Extracts required skills, experience requirements, and education keywords from job text.
2. **Resume Parsing**: Extracts raw text from uploaded `PDF` (via PyMuPDF) and `DOCX` (via python-docx) documents.
3. **Text Preprocessing**: Cleans noise, standardizes formatting, and normalizes technical terms.
4. **Information Extraction**: Extracts candidate name, contact info, skill lists, degree qualifications, and total work experience in years.
5. **Skill Matching**: Computes matched skills, missing skills, and overall skill coverage ratio.
6. **TF-IDF Similarity**: Measures sparse n-gram keyword similarity using scikit-learn `TfidfVectorizer` and cosine similarity.
7. **Semantic Similarity**: Measures dense contextual similarity using the `all-MiniLM-L6-v2` transformer model.
8. **Experience Scoring**: Evaluates candidate total experience against the required experience benchmark.
9. **Hybrid Score**: Combines all evaluation criteria into a unified score (0–100).
10. **Candidate Ranking**: Ranks candidates in descending order of their composite Hybrid Score.

---

## 4. Hybrid Scoring Formula

The candidate's composite **Hybrid Score** is calculated using the following experimental formula:

$$\text{Hybrid Score} = \Big( 0.35 \times \text{skill\_coverage} + 0.30 \times \text{semantic\_normalized} + 0.20 \times \text{tfidf\_normalized} + 0.15 \times \text{experience\_score} \Big) \times 100$$

> **Parameter Note**: These scoring weights are current project experimental parameters configured in `ai_engine/scoreing/hybrid_scorer.py` and may be tuned during ongoing evaluation.

---

## 5. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React + Vite Frontend                    │
│           (Candidate Dashboard, Actions, Table)             │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP REST API (JWT Bearer)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                        │
│          (Auth, Screening Routes, Resume Storage)          │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌─────────────────────────────┐  ┌────────────────────────────┐
│          MongoDB            │  │         AI Engine          │
│ (Users, Jobs, Candidates,   │  │ (Text Parsing, TF-IDF,     │
│    Screening Results)       │  │  Semantic Transformers)    │
└─────────────────────────────┘  └────────────────────────────┘
```

- **Frontend**: Single-page application built with React 18, Vite, and Tailwind CSS.
- **Backend**: Async RESTful API built with FastAPI and Uvicorn.
- **AI Engine**: Modular NLP processing package (`ai_engine/`).
- **Database**: Document database (MongoDB) with recruiter data isolation.

---

## 6. Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React
- **Backend**: Python 3.11+, FastAPI, Uvicorn, Pydantic, PyJWT, Argon2 (`pwdlib`)
- **Database**: MongoDB (`pymongo`)
- **AI / NLP**: PyMuPDF (`fitz`), python-docx, scikit-learn, SentenceTransformers (`all-MiniLM-L6-v2`), spaCy (`en_core_web_sm`), NLTK, NumPy, Pandas
- **Testing & DevOps**: Pytest, Docker, Docker Compose

---

## 7. Project Structure

```text
AI-Resume-Screening-System/
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── LICENSE
├── README.md
├── ai_engine/
│   ├── config/
│   ├── embeddings/
│   ├── extraction/
│   ├── matching/
│   ├── models/
│   ├── parser/
│   ├── preprocessing/
│   ├── ranking/
│   └── scoreing/            # Hybrid scoring implementation
├── backend/
│   ├── Dockerfile
│   ├── .env.example
│   ├── requirements.txt
│   ├── uploads/
│   │   └── resumes/          # Permanent physical resume storage
│   └── app/
│       ├── config/
│       ├── middleware/
│       ├── models/
│       ├── routes/
│       ├── schemas/
│       └── services/
├── data/
├── docs/
│   ├── ai-pipeline.md
│   ├── api.md
│   ├── architecture.md
│   ├── database.md
│   └── setup.md
├── frontend/
│   ├── Dockerfile
│   ├── .env.example
│   ├── package.json
│   └── src/
│       ├── api/
│       ├── components/
│       ├── pages/
│       └── utils/
├── notebook/
└── tests/
    ├── test_ai_engine.py
    ├── test_auth.py
    ├── test_backend_api.py
    ├── test_mongodb_integration.py
    └── test_resumes.py
```

---

## 8. Key Features

- **Multi-Format Parsing**: Automatic text extraction from `PDF`, `DOCX`, and `TXT` files.
- **Structured Information Extraction**: Automatic extraction of candidate name, contact details, skill taxonomy, education degree, and work experience years.
- **Dual Matching Framework**: Keyword-level sparse matching (TF-IDF) + context-level dense matching (SentenceTransformers).
- **Batch Screening**: Upload multiple candidate resumes and screen against a job description in a single operation.
- **Recruiter Security & Authentication**: JWT Bearer token authentication with Argon2 password hashing.
- **Recruiter Data Isolation**: Recruiter-scoped ownership across job postings, candidate records, screening results, and resumes.
- **Secure Resume Access**:
  - **View Resume**: Protected inline view endpoint (`GET /api/v1/resumes/{id}/view`) returning PDF binary stream for browser tab preview.
  - **Download Resume**: Protected attachment download endpoint (`GET /api/v1/resumes/{id}/download`) preserving original filename.
- **Portable Resume Storage**: Stores physical resume files in `backend/uploads/resumes/` while maintaining portable relative path representations (`uploads/resumes/resume_<id>.<ext>`) in MongoDB.

---

## 9. API Overview

| Method | Path | Auth | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | No | Register a recruiter account |
| `POST` | `/api/v1/auth/login` | No | Authenticate recruiter and receive JWT token |
| `GET` | `/api/v1/auth/me` | Yes | Retrieve current recruiter profile |
| `POST` | `/api/v1/parse-resume` | No | Parse resume text and extract candidate info |
| `POST` | `/api/v1/screen` | Yes | Screen single candidate resume against JD |
| `POST` | `/api/v1/screen-candidates` | Yes | Batch screen multiple candidate resumes against JD |
| `GET` | `/api/v1/jobs` | Yes | List recruiter job postings |
| `GET` | `/api/v1/jobs/{job_id}/results` | Yes | Retrieve ranked candidate results for a job |
| `GET` | `/api/v1/resumes/{resume_id}/view` | Yes | View original uploaded resume inline (PDF preview) |
| `GET` | `/api/v1/resumes/{resume_id}/download` | Yes | Download original uploaded resume as attachment |

*For complete endpoint request/response payloads, refer to [`docs/api.md`](docs/api.md).*

---

## 10. Local Setup & Quick Start

### Step 1: Environment Files
```powershell
Copy-Item backend\.env.example backend\.env
Copy-Item frontend\.env.example frontend\.env
```

### Step 2: Backend Setup
```powershell
# Create & activate virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install requirements & NLP models
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
.\.venv\Scripts\python.exe -m spacy download en_core_web_sm

# Launch FastAPI backend
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 3: Frontend Setup
```powershell
cd frontend
npm install
npm run dev
```
- Dashboard UI: `http://localhost:5173`
- Backend API Docs: `http://127.0.0.1:8000/docs`

---

## 11. Database Setup (MongoDB)

The backend connects to MongoDB (default: `mongodb://localhost:27017`) and uses database `ai_resume_screening_db`.

**Collections**:
- `users`: Recruiter account profiles & credentials.
- `jobs`: Recruiter job postings & required skills.
- `candidates`: Candidate profiles & parsed metadata.
- `resumes`: Resume document metadata & portable storage paths.
- `screening_results`: Screening scores, match breakdowns, and candidate rankings.

---

## 12. Testing & Verification

Run the automated test suite across all 48 integration and unit tests:

```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -m pytest
```

**Verification Status**:
- **Pytest**: `48 passed` (100% pass rate).
- **Frontend Build**: Verified (`npm run build` succeeds cleanly).
- **Real PDF Verification**: Verified real PDF upload, screening, inline view, and attachment download.

---

## 13. Docker Deployment

Launch multi-container setup via Docker Compose:

```powershell
docker-compose up --build -d
```

---

## 14. Security & Privacy Notes

- **Environment Files**: Never commit `.env` or production secrets to Git repositories.
- **JWT Secret**: Always use a cryptographically strong random secret for `JWT_SECRET_KEY` in production.
- **Recruiter Data Isolation**: All job postings, candidate records, and resume downloads enforce strict recruiter ownership checks (`user_id == recruiter_id`).
- **File Access Security**: Physical upload directories are not served statically; all file access requires JWT authentication.
- **Candidate Data Privacy**: Real candidate resumes contain personally identifiable information (PII). Use synthetic or anonymized resumes during development.

---

## 15. Current Project Status

> **Development Note**: Core AI and application components are under active development and integration. The current focus is integrating and validating the AI screening pipeline, backend APIs, database persistence, and frontend workflow.

---

## 16. Limitations

- **Information Extraction Variance**: Name and education extraction accuracy can vary across complex multi-column or non-standard resume layouts.
- **Experimental Weights**: Current hybrid scoring weights (35% skill, 30% semantic, 20% TF-IDF, 15% experience) are initial heuristic parameters.
- **OCR Support**: Scanned image-only PDF resumes require additional OCR preprocessing.
- **Decision Support**: The system provides decision support scoring and does not evaluate soft skills, interview performance, or non-textual qualifications.

---

## 17. Future Enhancements

- Fine-tuning sentence-transformers on domain-specific recruitment corpora.
- Expanding OCR support for scanned image-based PDF resumes.
- Interactive weight adjustment UI for recruiters to customize scoring criteria per job role.
- Advanced explainability metrics illustrating exact text snippets matching job requirements.

---

## 18. License

This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.  
Copyright (c) 2026 Akash Rauniyar.
