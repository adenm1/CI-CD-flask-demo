"""Routes module."""
from flask import Flask
from .api import api_bp
from .auth import auth_bp
from .health import health_bp
from .learning_sessions import learning_sessions_bp
from .pipelines import pipelines_bp


def register_routes(app: Flask) -> None:
    """Register all application routes.

    Args:
        app: Flask application instance
    """
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(learning_sessions_bp, url_prefix="/api/sessions")
    app.register_blueprint(pipelines_bp)
