"""Comprehensive Test Suite for JWT Authentication & Recruiter Authorization.

Tests:
1. Recruiter registration (success, duplicate email, weak password validation).
2. Recruiter login (success, wrong password, unknown email).
3. JWT creation, claims validation, and expiration.
4. /auth/me endpoint (authenticated vs unauthenticated vs expired token).
5. Protected endpoint access control (screening routes require valid Bearer token).
6. Recruiter data isolation (Recruiter A cannot access Recruiter B's jobs or screening results).
"""

import os
import unittest
from datetime import timedelta
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config.database import get_database
from backend.app.utils.security import create_access_token

client = TestClient(app)


class TestAuthenticationAndAuthorization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = get_database()
        cls.recruiter_a_email = "recruiter.a@example.com"
        cls.recruiter_b_email = "recruiter.b@example.com"
        cls.password = "SecurePass123!"

        # Ensure test user accounts are clean before running tests
        try:
            cls.db["users"].delete_many({"email": {"$in": [cls.recruiter_a_email, cls.recruiter_b_email]}})
            cls.db["jobs"].delete_many({"recruiter_id": {"$exists": True}})
            cls.db["candidates"].delete_many({"recruiter_id": {"$exists": True}})
            cls.db["resumes"].delete_many({"recruiter_id": {"$exists": True}})
            cls.db["screening_results"].delete_many({"recruiter_id": {"$exists": True}})
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            cls.db["users"].delete_many({"email": {"$in": [cls.recruiter_a_email, cls.recruiter_b_email]}})
            cls.db["jobs"].delete_many({"recruiter_id": {"$exists": True}})
            cls.db["candidates"].delete_many({"recruiter_id": {"$exists": True}})
            cls.db["resumes"].delete_many({"recruiter_id": {"$exists": True}})
            cls.db["screening_results"].delete_many({"recruiter_id": {"$exists": True}})
        except Exception:
            pass

    def test_01_register_user_success(self):
        """Test successful recruiter registration."""
        payload = {
            "name": "Recruiter Alice",
            "email": self.recruiter_a_email,
            "password": self.password,
        }
        res = client.post("/api/v1/auth/register", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["email"], self.recruiter_a_email)
        self.assertEqual(data["name"], "Recruiter Alice")
        self.assertEqual(data["role"], "recruiter")
        self.assertNotIn("password_hash", data)

    def test_02_register_duplicate_email_rejected(self):
        """Test registration with duplicate email returns 409 Conflict."""
        payload = {
            "name": "Recruiter Alice Duplicate",
            "email": self.recruiter_a_email,
            "password": self.password,
        }
        res = client.post("/api/v1/auth/register", json=payload)
        self.assertEqual(res.status_code, 409)
        self.assertIn("already exists", res.json()["detail"])

    def test_03_register_weak_password_rejected(self):
        """Test registration with short password (< 8 chars) returns 400 Bad Request or 422."""
        payload = {
            "name": "Short Pass User",
            "email": "shortpass@example.com",
            "password": "123",
        }
        res = client.post("/api/v1/auth/register", json=payload)
        self.assertIn(res.status_code, [400, 422])

    def test_04_login_success_and_jwt_returned(self):
        """Test successful login returns access_token and bearer token_type."""
        payload = {
            "email": self.recruiter_a_email,
            "password": self.password,
        }
        res = client.post("/api/v1/auth/login", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["token_type"], "bearer")

    def test_05_login_wrong_password_rejected(self):
        """Test login with wrong password returns 401 Unauthorized."""
        payload = {
            "email": self.recruiter_a_email,
            "password": "WrongPassword999",
        }
        res = client.post("/api/v1/auth/login", json=payload)
        self.assertEqual(res.status_code, 401)

    def test_06_login_unknown_email_rejected(self):
        """Test login with unregistered email returns 401 Unauthorized."""
        payload = {
            "email": "nonexistent@example.com",
            "password": self.password,
        }
        res = client.post("/api/v1/auth/login", json=payload)
        self.assertEqual(res.status_code, 401)

    def test_07_auth_me_success(self):
        """Test GET /api/v1/auth/me with valid Bearer token."""
        login_res = client.post(
            "/api/v1/auth/login",
            json={"email": self.recruiter_a_email, "password": self.password},
        )
        token = login_res.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        res = client.get("/api/v1/auth/me", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["email"], self.recruiter_a_email)

    def test_08_auth_me_missing_token(self):
        """Test GET /api/v1/auth/me without token returns 401 Unauthorized."""
        res = client.get("/api/v1/auth/me")
        self.assertEqual(res.status_code, 401)

    def test_09_auth_me_invalid_token(self):
        """Test GET /api/v1/auth/me with malformed token returns 401 Unauthorized."""
        headers = {"Authorization": "Bearer invalid_junk_token"}
        res = client.get("/api/v1/auth/me", headers=headers)
        self.assertEqual(res.status_code, 401)

    def test_10_auth_me_expired_token(self):
        """Test GET /api/v1/auth/me with expired token returns 401 Unauthorized."""
        user_doc = self.db["users"].find_one({"email": self.recruiter_a_email})
        self.assertIsNotNone(user_doc, "User doc for recruiter A must exist.")

        expired_token = create_access_token(
            data={"sub": user_doc["user_id"], "email": self.recruiter_a_email},
            expires_delta=timedelta(seconds=-10),
        )
        headers = {"Authorization": f"Bearer {expired_token}"}
        res = client.get("/api/v1/auth/me", headers=headers)
        self.assertEqual(res.status_code, 401)
        self.assertIn("expired", res.json()["detail"].lower())

    def test_11_protected_screening_endpoint_requires_auth(self):
        """Test GET /api/v1/jobs rejects request without token."""
        res = client.get("/api/v1/jobs")
        self.assertEqual(res.status_code, 401)

    def test_12_recruiter_data_isolation(self):
        """Test Recruiter A cannot access Recruiter B's jobs or screening results."""
        # 1. Register Recruiter B
        reg_b = client.post(
            "/api/v1/auth/register",
            json={
                "name": "Recruiter Bob",
                "email": self.recruiter_b_email,
                "password": self.password,
            },
        )
        self.assertEqual(reg_b.status_code, 201)

        # 2. Login Recruiter A and Recruiter B
        login_a = client.post(
            "/api/v1/auth/login",
            json={"email": self.recruiter_a_email, "password": self.password},
        ).json()["access_token"]

        login_b = client.post(
            "/api/v1/auth/login",
            json={"email": self.recruiter_b_email, "password": self.password},
        ).json()["access_token"]

        headers_a = {"Authorization": f"Bearer {login_a}"}
        headers_b = {"Authorization": f"Bearer {login_b}"}

        # 3. Recruiter A screens a batch and creates a job
        cand_bytes = b"Senior Accountant with 5 years experience in Excel, tax, auditing. Bachelor of Commerce."
        files = [("files", ("accountant.txt", cand_bytes, "text/plain"))]
        jd_text = "Looking for Accountant with Excel experience."

        screen_a = client.post(
            "/api/v1/screen-candidates",
            files=files,
            data={"job_description": jd_text, "job_title": "Recruiter A Job"},
            headers=headers_a,
        )
        self.assertEqual(screen_a.status_code, 200)

        # 4. Recruiter A lists jobs -> sees Recruiter A Job
        jobs_a = client.get("/api/v1/jobs", headers=headers_a).json()
        self.assertGreater(len(jobs_a), 0)
        job_a_id = jobs_a[0]["_id"]

        # 5. Recruiter B lists jobs -> should NOT see Recruiter A Job
        jobs_b = client.get("/api/v1/jobs", headers=headers_b).json()
        job_ids_b = [j["_id"] for j in jobs_b]
        self.assertNotIn(job_a_id, job_ids_b)

        # 6. Recruiter B tries to get results for Recruiter A's job_id -> 403 Forbidden
        res_b_access = client.get(
            f"/api/v1/jobs/{job_a_id}/results", headers=headers_b
        )
        self.assertEqual(res_b_access.status_code, 403)


if __name__ == "__main__":
    unittest.main()
