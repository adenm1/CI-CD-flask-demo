"""Registration request model for approval-based onboarding."""
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from backend.utils.db import Base


class RegistrationRequest(Base):
    """Represents a pending admin registration request."""

    __tablename__ = "registration_requests"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    reason = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, default="pending")  # pending, approved, rejected
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_by = Column(String(80), nullable=True)
    review_note = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
