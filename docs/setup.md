# Local Setup & Installation Guide

This document provides step-by-step instructions to configure, run, and test the **AI Resume Screening System** on a local development environment.

---

## Prerequisites

- **Python**: Version 3.11+
- **Node.js**: Version 18+ (with `npm`)
- **Database**: MongoDB 6.0+ (Local service or Docker container)
- **OS**: Windows / Linux / macOS

---

## 1. Environment Configuration

Copy environment template files:

```powershell
# Root / Backend environment file
Copy-Item backend\.env.example backend\.env

# Frontend environment file
Copy-Item frontend\.env.example frontend\.env
```

Ensure `backend/.env` contains your preferred MongoDB connection string and a secret JWT key:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=ai_resume_screening_db
JWT_SECRET_KEY=replace_with_a_long_random_secret_key
```

---

## 2. Python Backend Setup

### Create and Activate Virtual Environment

On Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Backend Dependencies

```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
```

### Download NLP Models

```powershell
.\.venv\Scripts\python.exe -m spacy download en_core_web_sm
```

### Start FastAPI Backend Server

```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

FastAPI Interactive API Documentation:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## 3. Frontend Dashboard Setup

Open a new terminal window in the `frontend` directory:

```powershell
cd frontend
npm install
npm run dev
```

The React frontend development server will launch at:
- Dashboard UI: `http://localhost:5173`

---

## 4. Run Test Suite

Run all automated integration, auth, MongoDB, and resume unit tests:

```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -m pytest
```

---

## 5. Docker Deployment (Optional)

To spin up MongoDB, FastAPI Backend, and React Frontend containers using Docker Compose:

```powershell
docker-compose up --build -d
```

Service URLs:
- Frontend Application: `http://localhost:5173`
- FastAPI Backend API: `http://localhost:8000`
- MongoDB Service: `mongodb://localhost:27017`
