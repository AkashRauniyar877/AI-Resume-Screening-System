"""Test suite for MongoDB Integration and End-to-End Batch Screening Persistence with JWT Auth.

Tests:
1. MongoDB connection & configuration.
2. Job CRUD operations.
3. Candidate CRUD operations.
4. Resume storage.
5. Screening Result CRUD operations.
6. End-to-End FastAPI + ai_engine + MongoDB batch screening workflow under authenticated recruiter account.
"""

import os
import unittest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config.database import get_database
from backend.app.services.job_service import JobService
from backend.app.services.candidate_service import CandidateService
from backend.app.services.resume_service import ResumeService
from backend.app.services.screening_service import ScreeningService

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
client = TestClient(app)


class TestMongoDBIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Use a test database to avoid touching production data
        cls.db = get_database("ai_resume_screening_test_db")
        cls.sample_pdf = os.path.join(
            PROJECT_ROOT, "data", "resumes", "data", "ACCOUNTANT", "10554236.pdf"
        )
        cls.email = "mongo_test_recruiter@example.com"
        cls.password = "Password123!"

        reg_res = client.post(
            "/api/v1/auth/register",
            json={"name": "Mongo Tester", "email": cls.email, "password": cls.password},
        )
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

    def setUp(self):
        self.job_service = JobService(self.db)
        self.candidate_service = CandidateService(self.db)
        self.resume_service = ResumeService(self.db)
        self.screening_service = ScreeningService(self.db)

    def test_01_mongodb_connection(self):
        """Test MongoDB ping connection and database instance."""
        client_obj = self.db.client
        ping = client_obj.admin.command("ping")
        self.assertEqual(ping.get("ok"), 1.0)
        self.assertEqual(self.db.name, "ai_resume_screening_test_db")

    def test_02_job_crud(self):
        """Test Job document creation and retrieval."""
        job_doc = self.job_service.create_job(
            job_title="Senior Python Engineer",
            job_description="Looking for Python and FastAPI expert.",
            required_skills=["python", "fastapi"],
            required_experience=3.0,
            required_education=["Bachelor of Science"],
        )
        self.assertIn("_id", job_doc)
        job_id = job_doc["_id"]

        fetched = self.job_service.get_job_by_id(job_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["job_title"], "Senior Python Engineer")

        all_jobs = self.job_service.list_jobs()
        self.assertGreater(len(all_jobs), 0)

    def test_03_candidate_crud(self):
        """Test Candidate document creation and retrieval."""
        cand_doc = self.candidate_service.create_or_update_candidate(
            candidate_id="test_cand_101",
            name="Alice Smith",
            email="alice@example.com",
            phone="555-0192",
            skills=["python", "sql"],
            education=["Bachelor of Engineering"],
            experience_years=4.0,
        )
        self.assertEqual(cand_doc["candidate_id"], "test_cand_101")

        fetched = self.candidate_service.get_candidate("test_cand_101")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["email"], "alice@example.com")

    def test_04_resume_crud(self):
        """Test Resume document creation and retrieval."""
        res_doc = self.resume_service.create_resume(
            resume_id="res_101",
            candidate_id="test_cand_101",
            filename="alice_resume.pdf",
            file_type=".pdf",
            extracted_text="Alice Smith software developer resume text...",
        )
        self.assertEqual(res_doc["resume_id"], "res_101")

        fetched = self.resume_service.get_resume("res_101")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["filename"], "alice_resume.pdf")

    def test_05_screening_result_crud(self):
        """Test Screening Result document creation and query."""
        scr_doc = self.screening_service.save_screening_result(
            job_id="test_job_1",
            candidate_id="test_cand_101",
            resume_id="res_101",
            matched_skills=["python"],
            missing_skills=["fastapi"],
            skill_coverage=50.0,
            tfidf_score=40.0,
            tfidf_normalized=80.0,
            semantic_score=60.0,
            semantic_normalized=70.0,
            experience_score=100.0,
            hybrid_score=75.5,
            rank=1,
        )
        self.assertEqual(scr_doc["job_id"], "test_job_1")

        results = self.screening_service.get_screening_results_for_job("test_job_1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["rank"], 1)
        self.assertEqual(results[0]["hybrid_score"], 75.5)

    def test_06_end_to_end_batch_screening_api(self):
        """Test End-to-End FastAPI + ai_engine + MongoDB batch screening endpoint under auth."""
        self.assertTrue(os.path.exists(self.sample_pdf))

        cand1_bytes = b"Senior Accountant with 5 years experience in accounting, excel, tax, auditing. Bachelor of Commerce."
        cand2_bytes = b"Python developer with 3 years experience in Python, FastAPI, SQL, React."
        jd_text = "We are looking for an Accountant with experience in accounting, excel, auditing. Bachelor of Commerce."

        files = [
            ("files", ("accountant_candidate.txt", cand1_bytes, "text/plain")),
            ("files", ("python_candidate.txt", cand2_bytes, "text/plain")),
        ]

        response = client.post(
            "/api/v1/screen-candidates",
            files=files,
            data={"job_description": jd_text, "job_title": "Lead Accountant"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_candidates"], 2)
        self.assertEqual(data["ranked_candidates"][0]["rank"], 1)

        # Verify MongoDB query endpoints with auth headers
        jobs_res = client.get("/api/v1/jobs", headers=self.auth_headers)
        self.assertEqual(jobs_res.status_code, 200)
        jobs = jobs_res.json()
        self.assertGreater(len(jobs), 0)

        latest_job_id = jobs[0]["_id"]
        results_res = client.get(
            f"/api/v1/jobs/{latest_job_id}/results", headers=self.auth_headers
        )
        self.assertEqual(results_res.status_code, 200)
        res_data = results_res.json()
        self.assertEqual(res_data["job_id"], latest_job_id)
        self.assertGreater(res_data["results_count"], 0)


if __name__ == "__main__":
    unittest.main()
