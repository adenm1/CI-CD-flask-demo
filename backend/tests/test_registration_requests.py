import base64
from datetime import datetime, timezone

import pytest
from sqlalchemy import text
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

from backend.utils import db


@pytest.fixture
def admin_keypair(client, admin_headers):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_pem = (
        private_key.public_key()
        .public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        .decode()
    )
    resp = client.post("/api/auth/keys", headers=admin_headers, json={"public_key": public_pem})
    assert resp.status_code == 200
    return private_key


def test_register_endpoint_disabled_by_default(client):
    resp = client.post("/api/auth/register", json={"username": "someone", "password": "secret123"})
    assert resp.status_code == 403
    assert resp.get_json()["error"] == "Self-registration is disabled. Please request access."


def test_can_create_registration_request(client):
    resp = client.post("/api/auth/register/request", json={"username": "new_user", "password": "secret123", "reason": "Need access"})
    assert resp.status_code == 202
    data = resp.get_json()
    assert data["request"]["status"] == "pending"
    request_id = data["request"]["id"]

    session = db.get_session()
    stored = session.execute(
        text("SELECT status FROM registration_requests WHERE id = :id"), {"id": request_id}
    ).scalar_one()
    assert stored == "pending"


def test_admin_can_approve_request(client, admin_headers, admin_keypair):
    create_resp = client.post("/api/auth/register/request", json={"username": "approve_me", "password": "secret123"})
    request_id = create_resp.get_json()["request"]["id"]

    signed_at = datetime.now(timezone.utc).isoformat()
    message = f"{request_id}:approve:{signed_at}"
    signature = base64.b64encode(
        admin_keypair.sign(message.encode(), padding.PKCS1v15(), hashes.SHA256())
    ).decode()

    approve_resp = client.post(
        f"/api/auth/register/requests/{request_id}/approve",
        headers=admin_headers,
        json={"note": "ok", "signature": signature, "signed_at": signed_at},
    )
    assert approve_resp.status_code == 200
    body = approve_resp.get_json()
    assert body["request"]["status"] == "approved"

    # New user can log in
    login_resp = client.post("/api/auth/login", json={"username": "approve_me", "password": "secret123"})
    assert login_resp.status_code == 200
    assert "token" in login_resp.get_json()


def test_admin_can_reject_request(client, admin_headers, admin_keypair):
    create_resp = client.post("/api/auth/register/request", json={"username": "reject_me", "password": "secret123"})
    request_id = create_resp.get_json()["request"]["id"]

    signed_at = datetime.now(timezone.utc).isoformat()
    message = f"{request_id}:reject:{signed_at}"
    signature = base64.b64encode(
        admin_keypair.sign(message.encode(), padding.PKCS1v15(), hashes.SHA256())
    ).decode()

    reject_resp = client.post(
        f"/api/auth/register/requests/{request_id}/reject",
        headers=admin_headers,
        json={"note": "not now", "signature": signature, "signed_at": signed_at},
    )
    assert reject_resp.status_code == 200
    assert reject_resp.get_json()["request"]["status"] == "rejected"

    # Rejected user should not exist
    login_resp = client.post("/api/auth/login", json={"username": "reject_me", "password": "secret123"})
    assert login_resp.status_code == 401
