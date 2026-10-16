# System Architecture

The **AI Resume Screening System** is designed as a decoupled, multi-tier web application that automates candidate resume parsing, semantic matching, hybrid scoring, candidate ranking, and recruiter workflows.

---

## High-Level Architecture Diagram

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

---

## Component Overview

### 1. Frontend Layer (`frontend/`)
- **Framework**: React 18 + Vite.
- **Styling**: Tailwind CSS with responsive layout components.
- **State & API**: Centralized `request()` wrapper (`frontend/src/api/client.js`) injecting JWT Authorization headers.
- **Key Views**:
  - Auth Page (Login/Registration)
  - Job Posting & Description Analysis View
  - Resume Batch Upload Page
  - Candidate Ranking & Results Table (`CandidateTable.jsx`, `CandidateDetails.jsx`)
  - Authenticated Resume **View Inline** (PDF browser preview via blob Object URLs)
  - Authenticated Resume **Download** (browser attachment download via blob Object URLs)

### 2. Backend Application Layer (`backend/app/`)
- **Framework**: FastAPI (Python 3.11+).
- **Authentication**: JWT tokens signed using `HS256`, password hashing with `Argon2` via `pwdlib`.
- **Router Modules**:
  - `/api/v1/auth`: User registration, login, token retrieval, current user info.
  - `/api/v1/screen` & `/screen-candidates`: Single and batch resume parsing and AI candidate screening.
  - `/api/v1/jobs` & `/api/v1/candidates`: Recruiter job postings and candidate records retrieval.
  - `/api/v1/resumes/{resume_id}/view` & `/download`: Recruiter-isolated physical file access endpoints.
- **Storage Layer**: Physical storage in `backend/uploads/resumes/resume_<resume_id>.<ext>` with portable relative paths stored in MongoDB.

### 3. AI Engine Layer (`ai_engine/`)
- **Parser**: PyMuPDF (`fitz`) for PDF parsing and `python-docx` for Word document text extraction.
- **Preprocessing**: RegEx cleaning, tokenization, stop-word removal, and normalization (`ai_engine/preprocessing`).
- **Information Extraction**: Name, contact details, skill recognition, education extraction, and experience calculation (`ai_engine/extraction`).
- **Matching & Vectorization**:
  - `TfidfVectorizer` with cosine similarity (`ai_engine/matching/tfidf_matcher.py`).
  - `SentenceTransformer` (`all-MiniLM-L6-v2`) for dense contextual semantic embeddings (`ai_engine/embeddings`).
- **Hybrid Scoring**: Combines skill coverage, semantic similarity, TF-IDF score, and experience score (`ai_engine/scoreing`).

### 4. Database Layer (`backend/app/config/database.py`)
- **Database Engine**: MongoDB (via `pymongo`).
- **Data Isolation**: Enforces `recruiter_id` ownership across users, jobs, candidate profiles, resume metadata, and screening results.
