"""API package."""
from flask import Flask
from flask_cors import CORS

from .routes import register_routes
from ..utils.db import Base, init_db
from ..utils.security import ensure_default_admin


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

    # Initialize Sentry for error tracking
    _init_sentry(app)

    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get("CORS_ORIGINS", ["http://localhost:5173"]),
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Initialize security features
    _init_security(app)

    # Initialize caching
    _init_cache(app)

    # Initialize rate limiting
    _init_rate_limiter(app)

    # Initialize monitoring
    _init_monitoring(app)

    # Initialize API documentation
    _init_swagger(app)

    # Initialize database connections
    engine = init_db(app)
    Base.metadata.create_all(bind=engine)

    with app.app_context():
        ensure_default_admin()

    # Setup logging
    _setup_logging(app)

    # Register routes
    register_routes(app)

    # Register error handlers
    _register_error_handlers(app)

    return app


def _init_sentry(app: Flask) -> None:
    """Initialize Sentry error tracking."""
    sentry_dsn = app.config.get("SENTRY_DSN")
    if sentry_dsn:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration

        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[FlaskIntegration()],
            traces_sample_rate=app.config.get("SENTRY_TRACES_SAMPLE_RATE", 1.0),
            environment=app.config.get("SENTRY_ENVIRONMENT", "development"),
            send_default_pii=False
        )
        app.logger.info("Sentry error tracking initialized")


def _init_security(app: Flask) -> None:
    """Initialize security headers and protections."""
    if app.config.get("TALISMAN_ENABLED", True):
        from flask_talisman import Talisman

        # Content Security Policy
        csp = {
            'default-src': "'self'",
            'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
            'style-src': ["'self'", "'unsafe-inline'"],
            'img-src': ["'self'", "data:", "https:"],
            'font-src': ["'self'", "data:"],
            'connect-src': ["'self'"]
        }

        Talisman(
            app,
            force_https=app.config.get("FORCE_HTTPS", False),
            strict_transport_security=True,
            content_security_policy=csp,
            content_security_policy_nonce_in=['script-src'],
            feature_policy={
                'geolocation': "'none'",
                'camera': "'none'",
                'microphone': "'none'"
            }
        )
        app.logger.info("Security headers initialized with Talisman")


def _init_cache(app: Flask) -> None:
    """Initialize caching with Redis."""
    from flask_caching import Cache

    cache_config = {
        'CACHE_TYPE': app.config.get('CACHE_TYPE', 'simple'),
        'CACHE_DEFAULT_TIMEOUT': app.config.get('CACHE_DEFAULT_TIMEOUT', 300),
    }

    if app.config.get('CACHE_TYPE') == 'redis':
        cache_config['CACHE_REDIS_URL'] = app.config.get('CACHE_REDIS_URL')

    cache = Cache(app, config=cache_config)
    app.extensions['cache'] = cache
    app.logger.info(f"Caching initialized with {cache_config['CACHE_TYPE']}")


def _init_rate_limiter(app: Flask) -> None:
    """Initialize rate limiting."""
    if app.config.get("RATELIMIT_ENABLED", True):
        from flask_limiter import Limiter
        from flask_limiter.util import get_remote_address

        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=[app.config.get("RATELIMIT_DEFAULT", "200 per day, 50 per hour")],
            storage_uri=app.config.get("RATELIMIT_STORAGE_URL", "memory://"),
            strategy="fixed-window"
        )
        app.extensions['limiter'] = limiter
        app.logger.info("Rate limiting initialized")


def _init_monitoring(app: Flask) -> None:
    """Initialize Prometheus monitoring."""
    if not app.config.get('ENABLE_METRICS', True):
        app.logger.info("Prometheus metrics disabled in config")
        return

    from prometheus_flask_exporter import PrometheusMetrics

    metrics = PrometheusMetrics(app)

    # Custom metrics
    metrics.info('app_info', 'Application info',
                 version=app.config.get('VERSION', '1.0.0'),
                 environment=app.config.get('FLASK_ENV', 'development'))

    app.extensions['metrics'] = metrics
    app.logger.info("Prometheus metrics initialized at /metrics")


def _init_swagger(app: Flask) -> None:
    """Initialize Swagger API documentation."""
    if app.config.get("SWAGGER_ENABLED", True):
        from flasgger import Swagger

        swagger_config = {
            "headers": [],
            "specs": [
                {
                    "endpoint": 'apispec',
                    "route": '/apispec.json',
                    "rule_filter": lambda rule: True,
                    "model_filter": lambda tag: True,
                }
            ],
            "static_url_path": "/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/api/docs/"
        }

        swagger_template = {
            "swagger": "2.0",
            "info": {
                "title": app.config.get("APP_NAME", "Flask API"),
                "description": "API documentation for CI/CD Flask Demo",
                "version": app.config.get("VERSION", "1.0.0"),
                "contact": {
                    "name": "API Support",
                    "email": "support@example.com"
                }
            },
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
                }
            },
            "security": [{"Bearer": []}]
        }

        Swagger(app, config=swagger_config, template=swagger_template)
        app.logger.info("Swagger API documentation initialized at /api/docs/")


def _setup_logging(app: Flask) -> None:
    """Configure application logging."""
    import logging

    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))

    if app.config.get("USE_STRUCTURED_LOGGING", False):
        from pythonjsonlogger import jsonlogger

        logHandler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
        logHandler.setFormatter(formatter)
        app.logger.addHandler(logHandler)
        app.logger.setLevel(log_level)
        app.logger.info("Structured JSON logging enabled")
    else:
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
