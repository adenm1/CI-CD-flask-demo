"""Stores risk-based authentication challenges."""
from datetime import datetime, timedelta, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from backend.utils.db import Base


def default_expiry() -> datetime:
    """Return default expiry (5 minutes)."""
    return datetime.now(timezone.utc) + timedelta(minutes=5)


class AuthChallenge(Base):
    """Represents a pending multi-factor challenge."""

    __tablename__ = "auth_challenges"

    id = Column(Integer, primary_key=True)
    admin_username = Column(String(80), nullable=False, index=True)
    method = Column(String(32), nullable=False)  # totp
    code_hash = Column(String(255), nullable=False)
    risk_score = Column(Integer, nullable=False, default=0)
    status = Column(String(32), nullable=False, default="pending")  # pending, passed, expired
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime(timezone=True), default=default_expiry, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
