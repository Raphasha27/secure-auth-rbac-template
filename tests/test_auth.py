from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["service"] == "Secure Auth + RBAC Template"

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}

def test_login_admin():
    res = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["role"] == "admin"

def test_login_invalid():
    res = client.post("/auth/login", json={"username": "admin", "password": "wrong"})
    assert res.status_code == 401

def test_me_authenticated():
    res = client.post("/auth/login", json={"username": "viewer", "password": "viewer123"})
    token = res.json()["access_token"]
    res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["username"] == "viewer"

def test_me_unauthenticated():
    res = client.get("/auth/me")
    assert res.status_code == 403

def test_admin_endpoint_allowed():
    res = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    token = res.json()["access_token"]
    res = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["message"] == "Welcome, admin"

def test_admin_endpoint_denied():
    res = client.post("/auth/login", json={"username": "viewer", "password": "viewer123"})
    token = res.json()["access_token"]
    res = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403

def test_write_endpoint_allowed():
    res = client.post("/auth/login", json={"username": "editor", "password": "editor123"})
    token = res.json()["access_token"]
    res = client.get("/write", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200

def test_write_endpoint_denied():
    res = client.post("/auth/login", json={"username": "viewer", "password": "viewer123"})
    token = res.json()["access_token"]
    res = client.get("/write", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403
