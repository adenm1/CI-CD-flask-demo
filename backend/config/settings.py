"""Application configuration settings."""
import os
from typing import Dict, Any


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

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # JSON
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    @staticmethod
    def init_app(app) -> None:
        """Initialize application with this config."""
        pass


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


config: Dict[str, Any] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestConfig,
    "default": DevelopmentConfig
}