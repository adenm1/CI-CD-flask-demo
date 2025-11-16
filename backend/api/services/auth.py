"""Authentication helpers and admin utilities."""
from typing import Optional

from backend.api.models import AdminUser
from backend.utils.db import get_session


def get_admin_by_username(username: str) -> Optional[AdminUser]:
    session = get_session()
    return session.query(AdminUser).filter(AdminUser.username == username).first()


def create_admin(username: str, password: str, role: str = "admin") -> AdminUser:
    """Create a new admin user."""
    session = get_session()

    # Check if username already exists
    existing = session.query(AdminUser).filter(AdminUser.username == username).first()
    if existing:
        raise ValueError("Username already exists")

    # Create new admin
    admin = AdminUser(username=username, role=role)
    admin.set_password(password)

    session.add(admin)
    session.commit()
    session.refresh(admin)

    return admin


def authenticate_admin(username: str, password: str) -> Optional[AdminUser]:
    admin = get_admin_by_username(username)
    if not admin or not admin.is_active:
        return None

    if not admin.check_password(password):
        return None

    return admin


def serialize_admin(admin: AdminUser) -> dict:
    return {
        "id": admin.id,
        "username": admin.username,
        "role": admin.role,
    }
