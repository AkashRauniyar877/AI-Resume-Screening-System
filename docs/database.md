# Database Architecture & Collections Schema

The system uses **MongoDB** as its primary document storage engine. All candidate profiles, job descriptions, resume metadata, and screening results are associated with a `recruiter_id` to enforce data isolation.

---

## Database Collections Overview

| Collection Name | Primary Key | Recruiter Isolated | Purpose |
| :--- | :--- | :--- | :--- |
| `users` | `user_id` | N/A | Recruiter user credentials and password hashes |
| `jobs` | `_id` (ObjectId) | Yes (`recruiter_id`) | Job position descriptions and extracted requirements |
| `candidates` | `candidate_id` | Yes (`recruiter_id`) | Parsed candidate profile records |
| `resumes` | `resume_id` | Yes (`recruiter_id`) | Resume document metadata and portable storage paths |
| `screening_results` | `job_id` + `candidate_id` | Yes (`recruiter_id`) | Hybrid scoring metrics and candidate rankings |

---

## Document Schemas

### 1. `users` Collection
```json
{
  "user_id": "usr_7ee8f92e9b6f451a",
  "name": "Jane Recruiter",
  "email": "recruiter@example.com",
  "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$...",
  "role": "recruiter",
  "created_at": "2026-09-30T12:00:00Z"
}
```

### 2. `jobs` Collection
```json
{
  "_id": "66f910a2b5e3c7a912345678",
  "job_title": "Senior Python Developer",
  "job_description": "We are seeking a Python developer with FastAPI and MongoDB experience...",
  "required_skills": ["Python", "FastAPI", "MongoDB"],
  "required_experience": 3.0,
  "required_education": ["Bachelor"],
  "recruiter_id": "usr_7ee8f92e9b6f451a",
  "created_at": "2026-09-30T12:05:00Z"
}
```

### 3. `resumes` Collection
```json
{
  "resume_id": "800b888ea6e1",
  "candidate_id": "cand_800b888ea6e1",
  "recruiter_id": "usr_7ee8f92e9b6f451a",
  "filename": "John_Doe_Resume.pdf",
  "original_filename": "John_Doe_Resume.pdf",
  "stored_filename": "resume_800b888ea6e1.pdf",
  "file_path": "uploads/resumes/resume_800b888ea6e1.pdf",
  "content_type": "application/pdf",
  "file_size": 27103,
  "file_type": ".pdf",
  "extracted_text": "Cleaned raw text extracted from PDF...",
  "created_at": "2026-09-30T12:10:00Z"
}
```

> **Path Portability Note**: The `file_path` field stores a relative path (`uploads/resumes/resume_<id>.<ext>`) to ensure portability across operating systems and deployment containers. Internal path resolution handles legacy absolute paths via `resolve_resume_path()`.

### 4. `screening_results` Collection
```json
{
  "job_id": "66f910a2b5e3c7a912345678",
  "candidate_id": "cand_800b888ea6e1",
  "resume_id": "800b888ea6e1",
  "recruiter_id": "usr_7ee8f92e9b6f451a",
  "rank": 1,
  "matched_skills": ["Python", "FastAPI"],
  "missing_skills": ["Docker"],
  "skill_coverage": 0.67,
  "tfidf_score": 0.75,
  "semantic_score": 0.82,
  "experience_score": 1.0,
  "hybrid_score": 82.4,
  "created_at": "2026-09-30T12:15:00Z"
}
```
