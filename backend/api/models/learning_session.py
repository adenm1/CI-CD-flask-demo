from datetime import datetime, timezone, tzinfo
from sqlalchemy import Column, Integer, String, Text, DateTime
from backend.utils.db import Base


def _utcnow():
    return datetime.now(timezone.utc)


def _serialize(value):
    if value is None :
        return None
    if value.tzinfo is None :
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()

class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="planned")  # planned/in_progress/completed
    difficulty = Column(String(50), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "difficulty": self.difficulty,
            "started_at": _serialize(self.started_at),
            "completed_at": _serialize(self.completed_at),
            "created_at": _serialize(self.created_at),
            "updated_at": _serialize(self.updated_at)
        }
