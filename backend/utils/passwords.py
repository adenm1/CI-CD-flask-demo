"""Password hashing helpers with optional pepper support."""
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash


def _get_pepper() -> str:
    return current_app.config.get("PASSWORD_PEPPER", "") if current_app else ""


def hash_password(raw_password: str) -> str:
    """Hash password with optional pepper."""
    pepper = _get_pepper()
    return generate_password_hash(raw_password + pepper)


def verify_password(raw_password: str, hashed: str) -> bool:
    """Verify password with optional pepper."""
    pepper = _get_pepper()
    return check_password_hash(hashed, raw_password + pepper)
