def test_create_session_success(client, admin_headers):
    payload = {"title": "Read PEP8", "status": "planned"}
    resp = client.post("/api/sessions/", json=payload, headers=admin_headers)
    assert resp.status_code == 201

    body = resp.get_json()
    assert "data" in body
    data = body["data"]

    assert data['id'] > 0
    assert data["title"] == payload["title"]
    assert data["status"] == payload["status"]
    assert data["created_at"].endswith("+00:00")


def test_create_session_missing_title(client, admin_headers):
    """Missing Title"""
    resp = client.post("/api/sessions/", json={"status": "planned"}, headers=admin_headers)
    assert resp.status_code == 400
    body = resp.get_json()
    assert "error" in body
    assert "title" in body["error"]


def test_create_session_invalid_status(client, admin_headers):
    resp = client.post("/api/sessions/", json={"title": "Bad status", "status": "done"}, headers=admin_headers)
    assert resp.status_code == 400
    assert "status" in resp.get_json()["error"]


def test_get_session_not_found(client, admin_headers):
    resp = client.get("/api/sessions/999", headers=admin_headers)
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Session not found"


def test_update_session_success(client, admin_headers):
    create_resp = client.post("/api/sessions/", json={"title": "Need update"}, headers=admin_headers)
    session_id = create_resp.get_json()["data"]["id"]

    update_resp = client.patch(
        f"/api/sessions/{session_id}",
        json={"status": "in_progress", "difficulty": "medium"},
        headers=admin_headers,
    )
    assert update_resp.status_code == 200
    data = update_resp.get_json()["data"]
    assert data["status"] == "in_progress"
    assert data["difficulty"] == "medium"


def test_update_session_missing(client, admin_headers):
    resp = client.patch("/api/sessions/999", json={"status": "completed"}, headers=admin_headers)
    assert resp.status_code == 404


def test_delete_session_success(client, admin_headers):
    create_resp = client.post("/api/sessions/", json={"title": "Temp"}, headers=admin_headers)
    session_id = create_resp.get_json()["data"]["id"]

    delete_resp = client.delete(f"/api/sessions/{session_id}", headers=admin_headers)
    assert delete_resp.status_code == 204


def test_delete_session_not_found(client, admin_headers):
    resp = client.delete("/api/sessions/999", headers=admin_headers)
    assert resp.status_code == 404


def test_list_sessions_order(client, admin_headers):
    first = client.post("/api/sessions/", json={"title": "First"}, headers=admin_headers)
    second = client.post("/api/sessions/", json={"title": "Second"}, headers=admin_headers)

    resp = client.get("/api/sessions/", headers=admin_headers)
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert len(data) >= 2
    assert data[0]["id"] == second.get_json()["data"]["id"]
    assert data[1]["id"] == first.get_json()["data"]["id"]
