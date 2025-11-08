"""API endpoints."""
from flask import Blueprint, jsonify, request, current_app
from datetime import datetime

api_bp = Blueprint("api", __name__)


@api_bp.route("/hello", methods=["GET"])
def hello():
    """Hello endpoint.

    Returns:
        JSON response with greeting message
    """
    current_app.logger.info("Hello endpoint called")

    return jsonify({
        "message": "Hello, this is your backend speaking!",
        "author": "Si Ying Liu",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@api_bp.route("/status", methods=["GET"])
def status():
    """Status endpoint.

    Returns:
        JSON response with system status
    """
    return jsonify({
        "status": "operational",
        "environment": current_app.config.get("ENV", "production"),
        "debug": current_app.debug,
        "timestamp": datetime.utcnow().isoformat()
    }), 200
