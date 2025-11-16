from flask import Blueprint, jsonify, request

from backend.api.services.learning_sessions import (
    create_session,
    delete_session,
    get_session_by_id,
    list_sessions,
    update_session
)
from .decorators import require_admin

learning_sessions_bp = Blueprint("learning_sessions", __name__)

@learning_sessions_bp.route("/", methods=["GET"])
@require_admin
def list_learning_sessions():
    """Return all learning sessions ordered by creation time."""
    sessions = list_sessions()
    return jsonify({
        "data": sessions
    }), 200

@learning_sessions_bp.route("/", methods=["POST"])
@require_admin
def create_learning_session():
    """Create a new learning session."""
    payload = request.get_json(silent=True) or {}
    try:
        session = create_session(payload)
        return jsonify({
            "data": session
        }), 201
    except ValueError as exc:
        return jsonify({
            "error": str(exc)
        }), 400

@learning_sessions_bp.route("/<int:session_id>", methods=["GET"])
@require_admin
def get_learning_session(session_id: int):
    """Return a single learning session by id."""
    session = get_session_by_id(session_id)
    if session is None:
        return jsonify({
            "error": "Session not found"
        }), 404
    return jsonify({
        "data": session
    }), 200

@learning_sessions_bp.route("/<int:session_id>", methods=["PATCH"])
@require_admin
def update_learning_session(session_id: int):
    """Update an existing learning session."""
    payload = request.get_json(silent=True) or {}
    try:
        session = update_session(session_id, payload)
    except ValueError as exc:
        return jsonify({
            "error": str(exc)
        }), 400

    if session is None:
        return jsonify({
            "error": "Session not found"
        }), 404

    return jsonify({
        "data": session
    }), 200

@learning_sessions_bp.route("/<int:session_id>", methods=["DELETE"])
@require_admin
def delete_learning_session(session_id: int):
    """Delete a learning session."""
    deleted = delete_session(session_id)
    if not deleted:
        return jsonify({
            "error": "Session not found"
        }), 404
    return "", 204
