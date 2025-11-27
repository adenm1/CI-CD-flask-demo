"""Security helpers for admin authentication."""
from typing import Optional

from flask import current_app
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from backend.utils.passwords import hash_password

from backend.api.models import AdminUser
from backend.utils.db import get_session


def _get_serializer() -> URLSafeTimedSerializer:
    secret = current_app.config["SECRET_KEY"]
    return URLSafeTimedSerializer(secret_key=secret, salt="admin-auth")


def generate_admin_token(admin: AdminUser) -> str:
    """Create a signed token for the admin user."""
    serializer = _get_serializer()
    return serializer.dumps({"admin_id": admin.id, "username": admin.username})


def verify_admin_token(token: str) -> Optional[AdminUser]:
    """Validate a token and return the admin user."""
    serializer = _get_serializer()
    max_age = current_app.config.get("AUTH_TOKEN_MAX_AGE", 60 * 60 * 12)

    try:
        payload = serializer.loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None

    session = get_session()
    admin = session.query(AdminUser).filter(AdminUser.id == payload.get("admin_id")).first()
    if not admin or not admin.is_active:
        return None

    return admin


def ensure_default_admin() -> None:
    """Create a default admin user when none exist."""
    if not current_app.config.get("ALLOW_DEFAULT_ADMIN_BOOTSTRAP", False):
        current_app.logger.info("Default admin bootstrap is disabled by ALLOW_DEFAULT_ADMIN_BOOTSTRAP=false")
        return

    session = get_session()
    username = current_app.config.get("DEFAULT_ADMIN_USERNAME", "admin")
    password = current_app.config.get("DEFAULT_ADMIN_PASSWORD", "change-me-now")

    existing = session.query(AdminUser).filter(AdminUser.username == username).first()
    if existing:
        return

    admin = AdminUser(username=username)
    admin.password_hash = hash_password(password)

    session.add(admin)
    session.commit()

    current_app.logger.warning(
        "Created default admin user '%s'. Update ADMIN_USERNAME/ADMIN_PASSWORD environment variables immediately.",
        username,
    )
