"""API package."""
from flask import Flask
from .routes import register_routes


def create_app(config_name: str = "default") -> Flask:
    """Application factory pattern.

    Args:
        config_name: Configuration name (development, production, testing)

    Returns:
        Configured Flask application instance
    """
    from ..config import config

    app = Flask(__name__)

    # Load configuration
    config_obj = config.get(config_name, config["default"])
    app.config.from_object(config_obj)
    config_obj.init_app(app)

    # Setup logging
    _setup_logging(app)

    # Register routes
    register_routes(app)

    # Register error handlers
    _register_error_handlers(app)

    return app


def _setup_logging(app: Flask) -> None:
    """Configure application logging."""
    import logging

    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))
    logging.basicConfig(
        level=log_level,
        format=app.config.get("LOG_FORMAT")
    )


def _register_error_handlers(app: Flask) -> None:
    """Register global error handlers."""
    from flask import jsonify
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle HTTP exceptions."""
        return jsonify({
            "error": error.name,
            "message": error.description,
            "status": error.code
        }), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Handle generic exceptions."""
        app.logger.error(f"Unhandled exception: {error}", exc_info=True)
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status": 500
        }), 500
