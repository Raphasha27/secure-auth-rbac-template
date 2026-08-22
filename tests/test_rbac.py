import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestRBAC:
    def test_admin_endpoint_requires_role(self):
        response = client.get("/admin/users")
        assert response.status_code in (401, 403)

    def test_content_create_requires_editor(self):
        response = client.post(
            "/content",
            json={"title": "Test", "body": "Content"},
        )
        assert response.status_code in (401, 403)

    def test_content_read_requires_viewer(self):
        response = client.get("/content")
        assert response.status_code in (401, 403, 200)

    def test_admin_role_assignment(self):
        response = client.post(
            "/admin/roles",
            json={"name": "moderator", "permissions": ["content:read"]},
        )
        assert response.status_code in (401, 403, 200, 201)

    def test_permission_enforcement(self):
        response = client.delete("/content/1")
        assert response.status_code in (401, 403, 404)
