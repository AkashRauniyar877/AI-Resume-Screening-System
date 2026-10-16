"""FastAPI Backend Integration Test Suite with JWT Authentication.

Tests endpoints:
1. POST /api/v1/parse-resume (Public)
2. POST /api/v1/screen (Protected)
3. POST /api/v1/screen-candidates (Protected)
4. Error handling for invalid file formats, missing fields, and unauthenticated access.
"""

import os
import unittest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config.database import get_database

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
client = TestClient(app)


class TestBackendAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = get_database("ai_resume_screening_test_api_db")
        cls.sample_pdf = os.path.join(
            PROJECT_ROOT, "data", "resumes", "data", "ACCOUNTANT", "10554236.pdf"
        )
        cls.sample_jd = """
        We are looking for an Accountant with experience in financial reporting,
        accounting, ledger maintenance, Excel, tax filings, and auditing.
        Bachelor's degree in Commerce or Accounting required.
        """
        # Register and login test recruiter to obtain JWT Bearer token
        cls.email = "api_test_recruiter@example.com"
        cls.password = "Password123!"

        reg_res = client.post(
            "/api/v1/auth/register",
            json={"name": "API Tester", "email": cls.email, "password": cls.password},
        )
        if reg_res.status_code not in (201, 409):
            raise RuntimeError(f"Failed to set up test recruiter: {reg_res.text}")

        login_res = client.post(
            "/api/v1/auth/login",
            json={"email": cls.email, "password": cls.password},
        )
        cls.token = login_res.json()["access_token"]
        cls.auth_headers = {"Authorization": f"Bearer {cls.token}"}

    @classmethod
    def tearDownClass(cls):
        try:
            cls.db["users"].delete_many({})
            cls.db["jobs"].delete_many({})
            cls.db["candidates"].delete_many({})
            cls.db["resumes"].delete_many({})
            cls.db["screening_results"].delete_many({})
        except Exception:
            pass

    def test_01_health_check(self):
        """Test GET / and GET /health."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

        health_res = client.get("/health")
        self.assertEqual(health_res.status_code, 200)
        self.assertEqual(health_res.json()["status"], "healthy")

    def test_02_parse_resume_success(self):
        """Test POST /api/v1/parse-resume with existing PDF sample."""
        self.assertTrue(os.path.exists(self.sample_pdf))

        with open(self.sample_pdf, "rb") as f:
            response = client.post(
                "/api/v1/parse-resume",
                files={"file": ("10554236.pdf", f, "application/pdf")},
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["filename"], "10554236.pdf")
        self.assertIn("ACCOUNTANT", data["extracted_text"].upper())
        self.assertIn("candidate_info", data)

    def test_03_parse_resume_invalid_extension(self):
        """Test POST /api/v1/parse-resume with unsupported file extension."""
        files = {"file": ("unsupported_image.png", b"fake image bytes", "image/png")}
        response = client.post("/api/v1/parse-resume", files=files)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported file type", response.json()["detail"])

    def test_04_screen_resume_success(self):
        """Test POST /api/v1/screen with PDF resume and job description (Authenticated)."""
        with open(self.sample_pdf, "rb") as f:
            response = client.post(
                "/api/v1/screen",
                files={"file": ("10554236.pdf", f, "application/pdf")},
                data={"job_description": self.sample_jd},
                headers=self.auth_headers,
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["filename"], "10554236.pdf")
        self.assertIn("candidate_info", data)
        self.assertIn("match_results", data)
        self.assertIn("hybrid_score", data["match_results"])
        self.assertGreaterEqual(data["match_results"]["hybrid_score"], 0.0)

    def test_05_screen_resume_unauthenticated_rejected(self):
        """Test POST /api/v1/screen without Bearer token returns 401 Unauthorized."""
        with open(self.sample_pdf, "rb") as f:
            response = client.post(
                "/api/v1/screen",
                files={"file": ("10554236.pdf", f, "application/pdf")},
                data={"job_description": self.sample_jd},
            )

        self.assertEqual(response.status_code, 401)

    def test_06_screen_resume_empty_jd(self):
        """Test POST /api/v1/screen with empty job description."""
        with open(self.sample_pdf, "rb") as f:
            response = client.post(
                "/api/v1/screen",
                files={"file": ("10554236.pdf", f, "application/pdf")},
                data={"job_description": "   "},
                headers=self.auth_headers,
            )

        self.assertIn(response.status_code, [400, 422])

    def test_07_screen_candidates_batch_success(self):
        """Test POST /api/v1/screen-candidates with multiple resumes (Authenticated)."""
        cand1_bytes = b"Senior Accountant with 5 years experience in accounting, excel, tax, auditing. Bachelor of Commerce."
        cand2_bytes = b"Python developer with 3 years experience in Python, FastAPI, SQL, React."

        files = [
            ("files", ("accountant_resume.txt", cand1_bytes, "text/plain")),
            ("files", ("python_resume.txt", cand2_bytes, "text/plain")),
        ]

        response = client.post(
            "/api/v1/screen-candidates",
            files=files,
            data={"job_description": self.sample_jd},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_candidates"], 2)
        self.assertIn("job_description_analysis", data)
        self.assertIn("ranked_candidates", data)

        ranked = data["ranked_candidates"]
        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0]["rank"], 1)
        self.assertEqual(ranked[1]["rank"], 2)
        self.assertGreaterEqual(ranked[0]["hybrid_score"], ranked[1]["hybrid_score"])


if __name__ == "__main__":
    unittest.main()
