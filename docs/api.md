# API Reference Specification

The FastAPI backend provides RESTful API endpoints for authentication, resume parsing, candidate screening, job management, and secure resume viewing/downloading.

Base URL: `http://127.0.0.1:8000/api/v1`

---

## Endpoint Summary

| Category | Method | Path | Auth Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| **System** | `GET` | `/` | No | System health check and API metadata |
| **Auth** | `POST` | `/api/v1/auth/register` | No | Register a new recruiter account |
| **Auth** | `POST` | `/api/v1/auth/login` | No | Authenticate recruiter and return JWT Bearer token |
| **Auth** | `GET` | `/api/v1/auth/me` | Yes | Get authenticated recruiter profile |
| **Parsing** | `POST` | `/api/v1/parse-resume` | No | Public endpoint to extract text and info from single resume |
| **Screening** | `POST` | `/api/v1/screen` | Yes | Screen single resume against a job description |
| **Screening** | `POST` | `/api/v1/screen-candidates` | Yes | Batch screen and rank multiple resumes against a JD |
| **Jobs** | `GET` | `/api/v1/jobs` | Yes | List all stored job postings for authenticated recruiter |
| **Jobs** | `GET` | `/api/v1/jobs/{job_id}/results` | Yes | Retrieve ranked candidate screening results for a job |
| **Resumes** | `GET` | `/api/v1/resumes/{resume_id}/view` | Yes | Protected inline view endpoint (`Content-Disposition: inline`) |
| **Resumes** | `GET` | `/api/v1/resumes/{resume_id}/download` | Yes | Protected download endpoint (`Content-Disposition: attachment`) |

---

## Detailed Endpoint Specifications

### Authentication Endpoints

#### 1. Register Recruiter
- **`POST /api/v1/auth/register`**
- **Request Body**:
  ```json
  {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "password": "Password123!"
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "user_id": "usr_9a8b7c6d",
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "role": "recruiter"
  }
  ```

#### 2. Recruiter Login
- **`POST /api/v1/auth/login`**
- **Request Body**:
  ```json
  {
    "email": "jane.doe@example.com",
    "password": "Password123!"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1Ni...",
    "token_type": "bearer"
  }
  ```

---

### Candidate Screening Endpoints

#### Batch Screen Candidates
- **`POST /api/v1/screen-candidates`**
- **Headers**: `Authorization: Bearer <token>`
- **Form Fields**:
  - `files`: List of resume files (`PDF`, `DOCX`, `TXT`)
  - `job_description`: Job description text string
  - `job_title`: Job position title (Optional)
- **Response** (`200 OK`):
  ```json
  {
    "total_candidates": 1,
    "job_description_analysis": {
      "required_skills": ["Python", "FastAPI", "MongoDB"],
      "required_experience": 3.0,
      "required_education": ["Bachelor"]
    },
    "ranked_candidates": [
      {
        "rank": 1,
        "candidate_id": "cand_e145cc1ef937",
        "resume_id": "e145cc1ef937",
        "filename": "john_doe_resume.pdf",
        "hybrid_score": 87.5,
        "candidate_info": {
          "name": "John Doe",
          "email": "john.doe@example.com",
          "phone": "+1-555-0199",
          "skills": ["Python", "FastAPI", "Docker", "MongoDB"],
          "education": ["B.S. Computer Science"],
          "experience_years": 4.5
        },
        "match_results": {
          "matched_skills": ["Python", "FastAPI", "MongoDB"],
          "missing_skills": [],
          "skill_coverage": 1.0,
          "tfidf_score": 0.78,
          "semantic_score": 0.85,
          "experience_score": 1.0,
          "hybrid_score": 87.5
        },
        "resume_actions": {
          "view_url": "/api/v1/resumes/e145cc1ef937/view",
          "download_url": "/api/v1/resumes/e145cc1ef937/download"
        }
      }
    ]
  }
  ```

---

### Resume File Management Endpoints

#### 1. View Original Resume Inline
- **`GET /api/v1/resumes/{resume_id}/view`**
- **Headers**: `Authorization: Bearer <token>`
- **Behavior**: Verifies recruiter ownership. Returns physical file with `Content-Disposition: inline; filename="<original_name>"`.

#### 2. Download Original Resume
- **`GET /api/v1/resumes/{resume_id}/download`**
- **Headers**: `Authorization: Bearer <token>`
- **Behavior**: Verifies recruiter ownership. Returns physical file with `Content-Disposition: attachment; filename="<original_name>"`.
