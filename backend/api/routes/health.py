"""Health check endpoints."""
from flask import Blueprint, jsonify
from datetime import datetime, timezone
from sqlalchemy import text

from backend.utils.db import get_session

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint.

    Returns:
        JSON response with health status
    """
    db_status = "unknown"
    status_code = 200
    session = None

    try:
        session = get_session()
        session.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "unhealthy"
        status_code = 500
    finally:
        if session:
            session.close()

    return (
        jsonify(
            {
                "status": "healthy" if status_code == 200 else "degraded",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "service": "flask-api",
                "dependencies": {"database": db_status},
            }
        ),
        status_code,
    )


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
