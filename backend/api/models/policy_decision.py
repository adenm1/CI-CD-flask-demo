"""Stores decisions returned by the policy engine."""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from backend.utils.db import Base


class PolicyDecision(Base):
    """Record of a policy evaluation for auditable actions."""

    __tablename__ = "policy_decisions"

    id = Column(Integer, primary_key=True)
    actor = Column(String(80), nullable=False)
    action = Column(String(80), nullable=False)
    decision = Column(String(32), nullable=False)  # allow, deny, challenge
    rules = Column(Text, nullable=False)  # comma-separated rule ids or JSON string
    evidence = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
