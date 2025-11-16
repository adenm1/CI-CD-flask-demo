"""Service layer for LearningSession operations."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.exc import SQLAlchemyError

from backend.api.models.learning_session import LearningSession
from backend.utils.db import get_session


VALID_STATUSES = {"planned", "in_progress", "completed"}


def _validate_payload(payload: Dict[str, Any], partial: bool = False) -> Optional[str]:
    """Validate incoming payload."""
    title = payload.get("title")
    status = payload.get("status")

    if not partial or "title" in payload:
        if not title or not isinstance(title, str):
            return "Field 'title' is required and must be a string."

    if status is not None and status not in VALID_STATUSES:
        return f"Field 'status' must be one of {', '.join(VALID_STATUSES)}."

    return None


def create_session(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new learning session."""
    error = _validate_payload(data)
    if error:
        raise ValueError(error)

    db_session = get_session()
    try:
        new_session = LearningSession(
            title=data["title"],
            description=data.get("description"),
            status=data.get("status", "planned"),
            difficulty=data.get("difficulty"),
            started_at=_parse_datetime(data.get("started_at")),
            completed_at=_parse_datetime(data.get("completed_at")),
        )
        db_session.add(new_session)
        db_session.commit()
        db_session.refresh(new_session)
        return new_session.to_dict()
    except SQLAlchemyError:
        db_session.rollback()
        raise
    finally:
        db_session.close()


def list_sessions() -> List[Dict[str, Any]]:
    """Return all sessions ordered by creation time."""
    db_session = get_session()
    try:
        records = (
            db_session.query(LearningSession)
            .order_by(LearningSession.created_at.desc())
            .all()
        )
        return [record.to_dict() for record in records]
    finally:
        db_session.close()


def get_session_by_id(session_id: int) -> Optional[Dict[str, Any]]:
    """Return a single session by id."""
    db_session = get_session()
    try:
        record = db_session.get(LearningSession, session_id)
        return record.to_dict() if record else None
    finally:
        db_session.close()


def update_session(session_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update an existing session."""
    if not data:
        raise ValueError("Update payload cannot be empty.")

    error = _validate_payload(data, partial=True)
    if error:
        raise ValueError(error)

    db_session = get_session()
    try:
        record = db_session.get(LearningSession, session_id)
        if not record:
            return None

        for field in ["title", "description", "status", "difficulty"]:
            if field in data:
                setattr(record, field, data[field])

        if "started_at" in data:
            record.started_at = _parse_datetime(data["started_at"])
        if "completed_at" in data:
            record.completed_at = _parse_datetime(data["completed_at"])

        record.updated_at = datetime.now(timezone.utc)

        db_session.commit()
        db_session.refresh(record)
        return record.to_dict()
    except (SQLAlchemyError, ValueError):
        db_session.rollback()
        raise
    finally:
        db_session.close()


def delete_session(session_id: int) -> bool:
    """Delete a session by id."""
    db_session = get_session()
    try:
        record = db_session.get(LearningSession, session_id)
        if not record:
            return False

        db_session.delete(record)
        db_session.commit()
        return True
    except SQLAlchemyError:
        db_session.rollback()
        raise
    finally:
        db_session.close()


def _parse_datetime(value: Any) -> Optional[datetime]:
    """Convert ISO strings to datetime objects."""
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError("Datetime fields must be ISO formatted strings.")
