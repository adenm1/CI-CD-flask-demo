from flask import Blueprint, jsonify, request

from backend.api.services.auth import authenticate_admin, create_admin, serialize_admin
from backend.utils.security import generate_admin_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def admin_login():
    """Authenticate an admin and return a signed token."""
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    admin = authenticate_admin(username, password)
    if not admin:
        return jsonify({"error": "Incorrect username or password."}), 401

    token = generate_admin_token(admin)
    return jsonify({"token": token, "admin": serialize_admin(admin)})


@auth_bp.route("/register", methods=["POST"])
def admin_register():
    """Register a new admin user."""
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
