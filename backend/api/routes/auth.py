from flask import Blueprint, jsonify, request, g, current_app
import pyotp

from backend.api.models import RegistrationRequest
from backend.api.routes.decorators import require_admin
from backend.api.services.auth import (
    authenticate_admin,
    create_admin,
    serialize_admin,
    create_registration_request,
    list_registration_requests,
    approve_registration_request,
    reject_registration_request,
    register_public_key,
    _verify_signature,
    log_audit_event,
    evaluate_login_risk,
    require_policy_for_action,
    handle_risk_challenge,
)
from backend.api.services.risk import calculate_risk
from backend.utils.security import generate_admin_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def admin_login():
    """Authenticate an admin and return a signed token."""
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    totp_code = (payload.get("totp_code") or "").strip() or None

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    admin = authenticate_admin(username, password)
    if not admin:
        return jsonify({"error": "Incorrect username or password."}), 401

    risk_score = evaluate_login_risk(username, request.remote_addr, 0)
    decision, rules, evidence = require_policy_for_action(admin, "auth.login", risk_score)
    if decision == "deny":
        return jsonify({"error": "Login denied by policy.", "rules": rules, "evidence": evidence}), 403

    try:
        challenge = handle_risk_challenge(admin, risk_score, totp_code)
    except ValueError as e:
        return jsonify({"error": str(e), "rules": rules, "evidence": evidence}), 409

    if challenge:
        return jsonify(
            {
                "error": "Additional verification required.",
                "challenge_id": challenge.id,
                "method": "totp",
                "risk_score": risk_score,
                "rules": rules,
                "evidence": evidence,
            }
        ), 409

    token = generate_admin_token(admin)
    log_audit_event(
        "auth.login.success",
        {"username": admin.username, "risk_score": risk_score, "rules": rules, "evidence": evidence},
    )
    return jsonify({"token": token, "admin": serialize_admin(admin), "risk_score": risk_score, "rules": rules})


@auth_bp.route("/register", methods=["POST"])
def admin_register():
    """Register a new admin user."""
    if not current_app.config.get("ENABLE_SELF_REGISTRATION", False):
        return jsonify({"error": "Self-registration is disabled. Please request access."}), 403

    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters."}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400

    try:
        admin = create_admin(username, password)
        token = generate_admin_token(admin)
        return jsonify({"token": token, "admin": serialize_admin(admin)}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Registration failed. Please try again."}), 500


@auth_bp.route("/register/request", methods=["POST"])
def admin_register_request():
    """Submit a registration request for approval."""
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    reason = (payload.get("reason") or "").strip() or None

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters."}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400

    try:
        reg_request = create_registration_request(username, password, reason)
        return (
            jsonify(
                {
                    "message": "Registration request submitted for approval.",
                    "request": serialize_registration_request(reg_request),
                }
            ),
            202,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Could not create registration request."}), 500


@auth_bp.route("/register/requests", methods=["GET"])
@require_admin
def list_register_requests():
    """List registration requests (admin only)."""
    status = request.args.get("status")
    requests = list_registration_requests(status)
    return jsonify({"requests": [serialize_registration_request(r) for r in requests]})


@auth_bp.route("/register/requests/<int:request_id>/approve", methods=["POST"])
@require_admin
def approve_request(request_id: int):
    """Approve a pending registration request and create the user."""
    payload = request.get_json(silent=True) or {}
    note = (payload.get("note") or "").strip() or None
    signature = (payload.get("signature") or "").strip()
    signed_at = (payload.get("signed_at") or "").strip()

    try:
        if not signature or not signed_at:
            return jsonify({"error": "Approval signature and signed_at are required."}), 400

        message = f"{request_id}:approve:{signed_at}"
        sig_hash = _verify_signature(g.current_admin, message, signature)

        risk_score = calculate_risk(request.remote_addr, failures=0)
        decision, rules, evidence = require_policy_for_action(g.current_admin, "register.approve", risk_score)
        if decision == "deny":
            return jsonify({"error": "Approval denied by policy.", "rules": rules, "evidence": evidence}), 403
        if decision == "challenge":
            return jsonify({"error": "Approval requires secondary validation.", "rules": rules, "evidence": evidence}), 409

        reg_request = approve_registration_request(request_id, g.current_admin, note)
        log_audit_event(
            "registration.approve",
            {"request_id": request_id, "reviewer": g.current_admin.username, "note": note, "signed_at": signed_at},
            signature_hash=sig_hash,
        )
        return jsonify(
            {
                "message": "Request approved and account created.",
                "request": serialize_registration_request(reg_request),
            }
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to approve request."}), 500


@auth_bp.route("/register/requests/<int:request_id>/reject", methods=["POST"])
@require_admin
def reject_request(request_id: int):
    """Reject a pending registration request."""
    payload = request.get_json(silent=True) or {}
    note = (payload.get("note") or "").strip() or None
    signature = (payload.get("signature") or "").strip()
    signed_at = (payload.get("signed_at") or "").strip()

    try:
        if not signature or not signed_at:
            return jsonify({"error": "Rejection signature and signed_at are required."}), 400

        message = f"{request_id}:reject:{signed_at}"
        sig_hash = _verify_signature(g.current_admin, message, signature)

        risk_score = calculate_risk(request.remote_addr, failures=0)
        decision, rules, evidence = require_policy_for_action(g.current_admin, "register.reject", risk_score)
        if decision == "deny":
            return jsonify({"error": "Rejection denied by policy.", "rules": rules, "evidence": evidence}), 403
        if decision == "challenge":
            return jsonify({"error": "Rejection requires secondary validation.", "rules": rules, "evidence": evidence}), 409

        reg_request = reject_registration_request(request_id, g.current_admin, note)
        log_audit_event(
            "registration.reject",
            {"request_id": request_id, "reviewer": g.current_admin.username, "note": note, "signed_at": signed_at},
            signature_hash=sig_hash,
        )
        return jsonify(
            {
                "message": "Request rejected.",
                "request": serialize_registration_request(reg_request),
            }
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to reject request."}), 500


def serialize_registration_request(req: RegistrationRequest) -> dict:
    """Serialize a registration request for API responses."""
    return {
        "id": req.id,
        "username": req.username,
        "reason": req.reason,
        "status": req.status,
        "reviewed_by": req.reviewed_by,
        "review_note": req.review_note,
        "created_at": req.created_at.isoformat() if req.created_at else None,
        "reviewed_at": req.reviewed_at.isoformat() if req.reviewed_at else None,
    }


@auth_bp.route("/keys", methods=["POST"])
@require_admin
def register_key():
    """Register approval public key for the current admin."""
    payload = request.get_json(silent=True) or {}
    public_key = (payload.get("public_key") or "").strip()
    if not public_key:
        return jsonify({"error": "public_key is required."}), 400

    try:
        register_public_key(g.current_admin, public_key)
        log_audit_event(
            "auth.key.register",
            {"admin": g.current_admin.username},
        )
        return jsonify({"message": "Public key registered."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/totp/enroll", methods=["POST"])
@require_admin
def enroll_totp():
    """Enroll TOTP for current admin."""
    if g.current_admin.totp_secret:
        return jsonify({"error": "TOTP already enrolled."}), 400

    secret = pyotp.random_base32()
    g.current_admin.totp_secret = secret
    # Persist
    from backend.utils.db import get_session

    session = get_session()
    session.add(g.current_admin)
    session.commit()

    log_audit_event("auth.totp.enroll", {"admin": g.current_admin.username})

    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=g.current_admin.username, issuer_name="CI-CD Dashboard")
    return jsonify({"secret": secret, "otpauth_uri": uri})
