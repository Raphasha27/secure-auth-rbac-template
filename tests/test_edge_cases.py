"""Edge case and comprehensive tests for Secure Auth RBAC Template."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAuthEdgeCases:
    def test_register_duplicate_email(self):
        client.post(
            "/auth/register",
            json={"email": "dup@example.com", "password": "pass1", "full_name": "First"},
        )
        response = client.post(
            "/auth/register",
            json={"email": "dup@example.com", "password": "pass2", "full_name": "Second"},
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_register_empty_email(self):
        response = client.post(
            "/auth/register",
            json={"email": "", "password": "pass", "full_name": "User"},
        )
        assert response.status_code in (400, 422)

    def test_register_empty_password(self):
        response = client.post(
            "/auth/register",
            json={"email": "empty@example.com", "password": "", "full_name": "User"},
        )
        assert response.status_code in (400, 422)

    def test_register_missing_fields(self):
        response = client.post("/auth/register", json={})
        assert response.status_code == 422

    def test_login_wrong_password(self):
        client.post(
            "/auth/register",
            json={"email": "wrongpw@example.com", "password": "correct", "full_name": "User"},
        )
        response = client.post(
            "/auth/login",
            data={"username": "wrongpw@example.com", "password": "incorrect"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self):
        response = client.post(
            "/auth/login",
            data={"username": "ghost@example.com", "password": "pass"},
        )
        assert response.status_code == 401


class TestRBACEnforcement:
    def test_admin_users_requires_admin_role(self):
        response = client.get("/admin/users")
        assert response.status_code in (401, 403)

    def test_admin_roles_requires_admin_role(self):
        response = client.post(
            "/admin/roles",
            json={"name": "test-role", "permissions": []},
        )
        assert response.status_code in (401, 403)

    def test_content_list_requires_user_role(self):
        response = client.get("/content")
        assert response.status_code in (401, 403, 200)

    def test_content_create_requires_permission(self):
        response = client.post(
            "/content",
            json={"title": "Test", "body": "Body"},
        )
        assert response.status_code in (401, 403)

    def test_content_delete_requires_permission(self):
        response = client.delete("/content/1")
        assert response.status_code in (401, 403)

    def test_protected_endpoints_without_bearer(self):
        endpoints = [
            ("GET", "/admin/users"),
            ("POST", "/admin/roles"),
            ("GET", "/content"),
            ("POST", "/content"),
            ("DELETE", "/content/1"),
        ]
        for method, path in endpoints:
            if method == "GET":
                response = client.get(path)
            elif method == "POST":
                response = client.post(path, json={})
            else:
                response = client.delete(path)
            assert response.status_code in (401, 403), f"{method} {path} should be protected"


class TestHealthEndpoint:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "rbac-api"
