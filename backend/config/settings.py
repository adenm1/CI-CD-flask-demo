"""Application configuration settings."""
import os
from typing import Dict, Any


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


class Config:
    """Base configuration."""

    # Application
    APP_NAME = "Flask CI/CD Demo"
    VERSION = "1.0.0"

    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    DEFAULT_ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    DEFAULT_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change-me-now")
    AUTH_TOKEN_MAX_AGE = int(os.getenv("AUTH_TOKEN_MAX_AGE", 60 * 60 * 12))  # 12 hours
    ENABLE_SELF_REGISTRATION = os.getenv("ENABLE_SELF_REGISTRATION", "false").lower() == "true"
    PASSWORD_PEPPER = os.getenv("PASSWORD_PEPPER", "")

    # Default admin bootstrap is disabled in production unless explicitly allowed
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    _allow_bootstrap_default = "true" if FLASK_ENV != "production" else "false"
    ALLOW_DEFAULT_ADMIN_BOOTSTRAP = (
        os.getenv("ALLOW_DEFAULT_ADMIN_BOOTSTRAP", _allow_bootstrap_default).lower() == "true"
    )

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    USE_STRUCTURED_LOGGING = os.getenv("USE_STRUCTURED_LOGGING", "false").lower() == "true"

    # JSON
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    # Redis & Caching
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TYPE = os.getenv("CACHE_TYPE", "redis")
    CACHE_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "300"))

    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv("RATELIMIT_ENABLED", "true").lower() == "true"
    RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "200 per day, 50 per hour")

    # Security Headers
    TALISMAN_ENABLED = os.getenv("TALISMAN_ENABLED", "true").lower() == "true"
    FORCE_HTTPS = os.getenv("FORCE_HTTPS", "false").lower() == "true"

    # Monitoring
    SENTRY_DSN = os.getenv("SENTRY_DSN", "")
    SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT", "development")
    SENTRY_TRACES_SAMPLE_RATE = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0"))

    # API Documentation
    SWAGGER_ENABLED = os.getenv("SWAGGER_ENABLED", "true").lower() == "true"

    # Database
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB = os.getenv("POSTGRES_DB", "learning_env")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
    }

    @staticmethod
    def init_app(app) -> None:
        """Initialize application with this config."""
        _ensure_sqlite_path(app)


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    TESTING = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False

    @staticmethod
    def init_app(app) -> None:
        """Initialize production app."""
        Config.init_app(app)

        # Production-specific initialization
        import logging
        from logging.handlers import RotatingFileHandler

        if not os.path.exists("logs"):
            os.mkdir("logs")

        file_handler = RotatingFileHandler(
            "logs/app.log",
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(Config.LOG_FORMAT)
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class TestConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True

    # Disable features that require external services in testing
    CACHE_TYPE = "SimpleCache"  # Use in-memory cache instead of Redis
    RATELIMIT_ENABLED = False  # Disable rate limiting in tests
    SENTRY_DSN = ""  # Disable Sentry in tests
    ENABLE_METRICS = False  # Disable Prometheus metrics


def _ensure_sqlite_path(app) -> None:
    """Ensure sqlite db URIs use absolute paths so cwd doesn't matter."""
    uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    if not uri or not uri.startswith("sqlite:///"):
        return

    relative_path = uri.replace("sqlite:///", "", 1)
    if relative_path.startswith(os.sep):
        return

    abs_path = os.path.abspath(os.path.join(PROJECT_ROOT, relative_path))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{abs_path}"


config: Dict[str, Any] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestConfig,
    "default": DevelopmentConfig
}
