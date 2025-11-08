"""Routes module."""
from flask import Flask
from .health import health_bp
from .api import api_bp


def register_routes(app: Flask) -> None:
    """Register all application routes.

    Args:
        app: Flask application instance
    """
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
