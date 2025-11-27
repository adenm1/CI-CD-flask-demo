"""Authentication helpers and admin utilities."""
from datetime import datetime, timezone
from typing import Optional
import base64
import hashlib
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from backend.api.models import (
    AdminUser,
    ApprovalKey,
    AuditEvent,
    AuthChallenge,
    RegistrationRequest,
)
from backend.api.services.policy import evaluate_action, persist_decision
from backend.api.services.risk import calculate_risk, issue_totp_challenge, verify_totp
from backend.utils.db import get_session
from backend.utils.passwords import hash_password, verify_password


def get_admin_by_username(username: str) -> Optional[AdminUser]:
    session = get_session()
    return session.query(AdminUser).filter(AdminUser.username == username).first()


def create_admin(username: str, password: str, role: str = "admin", password_hash: Optional[str] = None) -> AdminUser:
    """Create a new admin user."""
    session = get_session()

    # Check if username already exists
    existing = session.query(AdminUser).filter(AdminUser.username == username).first()
    if existing:
        raise ValueError("Username already exists")

    # Create new admin
    admin = AdminUser(username=username, role=role)
    if password_hash:
        admin.password_hash = password_hash
    else:
        admin.password_hash = hash_password(password)

    session.add(admin)
    session.commit()
    session.refresh(admin)

    return admin


def authenticate_admin(username: str, password: str) -> Optional[AdminUser]:
    admin = get_admin_by_username(username)
    if not admin or not admin.is_active:
        return None

    if not verify_password(password, admin.password_hash):
        return None

    return admin


def evaluate_login_risk(username: str, remote_addr: Optional[str], failures: int = 0) -> int:
    """Wrap risk calculation for login attempts."""
    return calculate_risk(remote_addr, failures)


def require_policy_for_action(admin: AdminUser, action: str, risk_score: int) -> tuple[str, list, dict]:
    """Evaluate and persist policy decision."""
    decision, rules, evidence = evaluate_action(admin.username, action, {"risk_score": risk_score})
    persist_decision(admin.username, action, decision, rules, evidence)
    return decision, rules, evidence


def serialize_admin(admin: AdminUser) -> dict:
    return {
        "id": admin.id,
        "username": admin.username,
        "role": admin.role,
        "has_totp": bool(admin.totp_secret),
    }


def register_public_key(admin: AdminUser, public_key_pem: str) -> ApprovalKey:
    """Register or replace an admin's approval public key."""
    session = get_session()
    existing = session.query(ApprovalKey).filter(ApprovalKey.admin_id == admin.id).first()
    if existing:
        existing.public_key_pem = public_key_pem
        existing.created_at = datetime.now(timezone.utc)
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing

    key = ApprovalKey(admin_id=admin.id, public_key_pem=public_key_pem)
    session.add(key)
    session.commit()
    session.refresh(key)
    return key


def _verify_signature(admin: AdminUser, message: str, signature_b64: str) -> str:
    """Verify signature with stored public key. Returns signature hash."""
    session = get_session()
    key = session.query(ApprovalKey).filter(ApprovalKey.admin_id == admin.id).first()
    if not key:
        raise ValueError("No approval public key registered for this admin.")

    try:
        signature_bytes = base64.b64decode(signature_b64)
    except Exception:
        raise ValueError("Signature is not valid base64.")

    public_key = load_pem_public_key(key.public_key_pem.encode())
    try:
        public_key.verify(
            signature_bytes,
            message.encode(),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    except Exception:
        raise ValueError("Signature verification failed.")

    return hashlib.sha256(signature_bytes).hexdigest()


def log_audit_event(event_type: str, payload: dict, signature_hash: Optional[str] = None) -> AuditEvent:
    """Persist an append-only audit record."""
    session = get_session()
    record = AuditEvent(
        event_type=event_type,
        payload=json.dumps(payload, default=str),
        signature_hash=signature_hash,
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def create_registration_request(username: str, password: str, reason: Optional[str] = None) -> RegistrationRequest:
    """Create a pending registration request."""
    session = get_session()

    existing_user = session.query(AdminUser).filter(AdminUser.username == username).first()
    if existing_user:
        raise ValueError("Username already exists")

    existing_request = (
        session.query(RegistrationRequest)
        .filter(RegistrationRequest.username == username, RegistrationRequest.status == "pending")
        .first()
    )
    if existing_request:
        raise ValueError("A pending request already exists for this username")

    request = RegistrationRequest(
        username=username,
        password_hash=hash_password(password),
        reason=reason,
    )

    session.add(request)
    session.commit()
    session.refresh(request)
    return request


def list_registration_requests(status: Optional[str] = None) -> list[RegistrationRequest]:
    """List registration requests filtered by status."""
    session = get_session()
    query = session.query(RegistrationRequest)
    if status:
        query = query.filter(RegistrationRequest.status == status)
    return query.order_by(RegistrationRequest.created_at.desc()).all()


def approve_registration_request(request_id: int, reviewer: AdminUser, note: Optional[str] = None) -> RegistrationRequest:
    """Approve a registration request and create the admin user."""
    session = get_session()
    request = session.query(RegistrationRequest).filter(RegistrationRequest.id == request_id).first()
    if not request or request.status != "pending":
        raise ValueError("Request not found or already processed")

    create_admin(username=request.username, password="", password_hash=request.password_hash)

    request.status = "approved"
    request.reviewed_by = reviewer.username
    request.review_note = note
    request.reviewed_at = datetime.now(timezone.utc)
    session.add(request)
    session.commit()
    session.refresh(request)
    return request


def reject_registration_request(request_id: int, reviewer: AdminUser, note: Optional[str] = None) -> RegistrationRequest:
    """Reject a registration request."""
    session = get_session()
    request = session.query(RegistrationRequest).filter(RegistrationRequest.id == request_id).first()
    if not request or request.status != "pending":
        raise ValueError("Request not found or already processed")

    request.status = "rejected"
    request.reviewed_by = reviewer.username
    request.review_note = note
    request.reviewed_at = datetime.now(timezone.utc)
    session.add(request)
    session.commit()
    session.refresh(request)
    return request


def handle_risk_challenge(admin: AdminUser, risk_score: int, totp_code: Optional[str]) -> Optional[AuthChallenge]:
    """Require TOTP when risk is elevated."""
    if risk_score < 40:
        return None

    if not admin.totp_secret:
        # Can't enforce TOTP without a secret; log and allow login so admin can enroll
        log_audit_event(
            "auth.risk.totp_missing",
            {"username": admin.username, "risk_score": risk_score},
        )
        return None

    if not totp_code:
        # issue placeholder challenge record
        challenge = issue_totp_challenge(admin.username, risk_score)
        return challenge

    if not verify_totp(admin, totp_code):
        raise ValueError("Invalid TOTP code.")

    return None
