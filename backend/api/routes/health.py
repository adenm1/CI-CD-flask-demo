"""Health check endpoints."""
from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint.

    Returns:
        JSON response with health status
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "flask-api"
    }), 200


@health_bp.route("/", methods=["GET"])
def index():
    """Root endpoint.

    Returns:
        JSON response with API information
    """
    return jsonify({
        "message": "Flask CI/CD Demo API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "api": "/api"
        }
    }), 200
