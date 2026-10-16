"""Test suite for Resume View and Download features and recruiter security isolation."""

import os
import unittest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.auth_service import AuthService
from backend.app.services.resume_service import ResumeService
from backend.app.utils.file_handler import UPLOAD_DIR, resolve_resume_path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
client = TestClient(app)


class TestResumeEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.auth_service = AuthService()

        # Recruiter A
        cls.user_a_email = "recruiter_a_view@example.com"
        cls.user_a_pwd = "Password123!"
        try:
            cls.auth_service.register_user("Recruiter A", cls.user_a_email, cls.user_a_pwd)
        except Exception:
            pass
        token_doc_a = cls.auth_service.authenticate_user(cls.user_a_email, cls.user_a_pwd)
        user_doc_a = cls.auth_service.get_user_by_email(cls.user_a_email)
        cls.token_a = token_doc_a["access_token"]
        cls.user_a_id = user_doc_a["user_id"]
        cls.headers_a = {"Authorization": f"Bearer {cls.token_a}"}

        # Recruiter B
        cls.user_b_email = "recruiter_b_view@example.com"
        cls.user_b_pwd = "Password123!"
        try:
            cls.auth_service.register_user("Recruiter B", cls.user_b_email, cls.user_b_pwd)
        except Exception:
            pass
        token_doc_b = cls.auth_service.authenticate_user(cls.user_b_email, cls.user_b_pwd)
        user_doc_b = cls.auth_service.get_user_by_email(cls.user_b_email)
        cls.token_b = token_doc_b["access_token"]
        cls.user_b_id = user_doc_b["user_id"]
        cls.headers_b = {"Authorization": f"Bearer {cls.token_b}"}

    def setUp(self):
        pdf_path = os.path.join(PROJECT_ROOT, "data", "resumes", "data", "ACCOUNTANT", "10554236.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                self.sample_resume_content = f.read()
        else:
            self.sample_resume_content = b"%PDF-1.4 Minimal PDF content"
        self.sample_jd = "Looking for an Accountant with experience in financial reporting and auditing."

    def test_01_upload_and_store_resume_file(self):
        """Test uploading a resume file saves physical file and MongoDB metadata."""
        files = {"file": ("test_john_doe.pdf", self.sample_resume_content, "application/pdf")}
        data = {"job_description": self.sample_jd, "job_title": "Python Developer"}

        res = client.post("/api/v1/screen", files=files, data=data, headers=self.headers_a)
        self.assertEqual(res.status_code, 200)

        json_data = res.json()
        self.assertIn("resume_id", json_data)
        self.assertIsNotNone(json_data["resume_id"])

        resume_id = json_data["resume_id"]

        # Verify MongoDB metadata
        resume_svc = ResumeService()
        doc = resume_svc.get_resume(resume_id, recruiter_id=self.user_a_id)
        self.assertIsNotNone(doc)
        self.assertEqual(doc["original_filename"], "test_john_doe.pdf")
        self.assertEqual(doc["content_type"], "application/pdf")
        self.assertEqual(doc["recruiter_id"], self.user_a_id)

        # Verify Physical File exists on disk
        abs_path = resolve_resume_path(doc["file_path"])
        self.assertTrue(os.path.exists(abs_path), f"File missing at {abs_path}")

    def test_02_view_resume_success(self):
        """Test recruiter viewing their own uploaded resume inline."""
        files = {"file": ("alice_view.pdf", self.sample_resume_content, "application/pdf")}
        res_upload = client.post("/api/v1/screen", files=files, data={"job_description": self.sample_jd}, headers=self.headers_a)
        resume_id = res_upload.json()["resume_id"]

        res_view = client.get(f"/api/v1/resumes/{resume_id}/view", headers=self.headers_a)
        self.assertEqual(res_view.status_code, 200)
        self.assertIn("inline", res_view.headers.get("content-disposition", ""))
        self.assertIn(self.sample_resume_content, res_view.content)

    def test_03_download_resume_success(self):
        """Test recruiter downloading their own uploaded resume as attachment."""
        files = {"file": ("bob_download.pdf", self.sample_resume_content, "application/pdf")}
        res_upload = client.post("/api/v1/screen", files=files, data={"job_description": self.sample_jd}, headers=self.headers_a)
        resume_id = res_upload.json()["resume_id"]

        res_dl = client.get(f"/api/v1/resumes/{resume_id}/download", headers=self.headers_a)
        self.assertEqual(res_dl.status_code, 200)
        self.assertIn("attachment", res_dl.headers.get("content-disposition", ""))
        self.assertIn("bob_download.pdf", res_dl.headers.get("content-disposition", ""))
        self.assertIn(self.sample_resume_content, res_dl.content)

    def test_04_recruiter_ownership_isolation_view(self):
        """Test Recruiter B cannot view Recruiter A's resume (403 Forbidden)."""
        files = {"file": ("secret_a.pdf", self.sample_resume_content, "application/pdf")}
        res_upload = client.post("/api/v1/screen", files=files, data={"job_description": self.sample_jd}, headers=self.headers_a)
        resume_id = res_upload.json()["resume_id"]

        # Recruiter B attempts to view Recruiter A's resume
        res_view_b = client.get(f"/api/v1/resumes/{resume_id}/view", headers=self.headers_b)
        self.assertEqual(res_view_b.status_code, 403)

    def test_05_recruiter_ownership_isolation_download(self):
        """Test Recruiter B cannot download Recruiter A's resume (403 Forbidden)."""
        files = {"file": ("secret_a_dl.pdf", self.sample_resume_content, "application/pdf")}
        res_upload = client.post("/api/v1/screen", files=files, data={"job_description": self.sample_jd}, headers=self.headers_a)
        resume_id = res_upload.json()["resume_id"]

        # Recruiter B attempts to download Recruiter A's resume
        res_dl_b = client.get(f"/api/v1/resumes/{resume_id}/download", headers=self.headers_b)
        self.assertEqual(res_dl_b.status_code, 403)

    def test_06_missing_resume_404(self):
        """Test non-existent resume_id returns 404 Not Found."""
        res = client.get("/api/v1/resumes/non_existent_resume_9999/view", headers=self.headers_a)
        self.assertEqual(res.status_code, 404)

    def test_07_unauthenticated_request_401(self):
        """Test viewing/downloading without JWT returns 401 Unauthorized."""
        files = {"file": ("unauth_test.pdf", self.sample_resume_content, "application/pdf")}
        res_upload = client.post("/api/v1/screen", files=files, data={"job_description": self.sample_jd}, headers=self.headers_a)
        resume_id = res_upload.json()["resume_id"]

        res_no_auth = client.get(f"/api/v1/resumes/{resume_id}/view")
        self.assertEqual(res_no_auth.status_code, 401)


if __name__ == "__main__":
    unittest.main()
