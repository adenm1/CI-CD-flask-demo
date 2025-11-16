def test_login_success(client):
    resp = client.post("/api/auth/login", json={"username": "test_admin", "password": "super-secret"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert "token" in body
    assert body["admin"]["username"] == "test_admin"


def test_login_invalid_credentials(client):
    resp = client.post("/api/auth/login", json={"username": "test_admin", "password": "wrong"})
    assert resp.status_code == 401
    assert "error" in resp.get_json()


def test_sessions_require_auth(client):
    resp = client.get("/api/sessions/")
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Authentication required."
