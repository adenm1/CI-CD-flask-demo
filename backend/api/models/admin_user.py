from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from backend.utils.db import Base
from backend.utils.passwords import hash_password, verify_password


class AdminUser(Base):
    """Administrative user with basic role information."""

    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False, default="admin")
    is_active = Column(Boolean, default=True, nullable=False)
    totp_secret = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    def set_password(self, raw_password: str) -> None:
        """Hash and set the password."""
        self.password_hash = hash_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Return True when the password matches the stored hash."""
        return verify_password(raw_password, self.password_hash)
