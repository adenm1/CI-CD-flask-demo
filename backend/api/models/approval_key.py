"""Public key registry for admin approval signatures."""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from backend.utils.db import Base


class ApprovalKey(Base):
    """Stores admin public keys used to sign approval decisions."""

    __tablename__ = "approval_keys"
    __table_args__ = (UniqueConstraint("admin_id", name="uq_approval_keys_admin"),)

    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey("admin_users.id"), nullable=False)
    public_key_pem = Column(String(2000), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
