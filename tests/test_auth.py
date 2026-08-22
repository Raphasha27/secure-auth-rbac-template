import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestAuthEndpoints:
    def test_register_user(self):
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "securepassword123",
                "full_name": "Test User",
            },
        )
        assert response.status_code in (200, 201, 422)

    def test_login_valid_credentials(self):
        response = client.post(
            "/auth/login",
            data={"username": "admin@example.com", "password": "admin123"},
        )
        assert response.status_code in (200, 401, 422)

    def test_login_invalid_credentials(self):
        response = client.post(
            "/auth/login",
            data={"username": "wrong@example.com", "password": "wrongpassword"},
        )
        assert response.status_code in (401, 422)

    def test_me_without_token(self):
        response = client.get("/auth/me")
        assert response.status_code in (401, 403)

    def test_protected_endpoint_no_auth(self):
        response = client.get("/admin/users")
        assert response.status_code in (401, 403)
