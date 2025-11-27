"""Append-only audit log with optional signature hash."""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from backend.utils.db import Base


class AuditEvent(Base):
    """Stores immutable audit records."""

    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True)
    event_type = Column(String(100), nullable=False)
    payload = Column(Text, nullable=False)
    signature_hash = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
