"""Audit streaming endpoints."""
import json
import time
from flask import Blueprint, Response, request, stream_with_context

from backend.api.models import AuditEvent
from backend.api.routes.decorators import require_admin
from backend.utils.db import get_session

audit_bp = Blueprint("audit", __name__, url_prefix="/api/audit")


def _format_event(event: AuditEvent) -> str:
    return f"data: {json.dumps({'id': event.id, 'event_type': event.event_type, 'payload': event.payload, 'signature_hash': event.signature_hash, 'created_at': event.created_at.isoformat() if event.created_at else None})}\n\n"  # noqa: E501


@audit_bp.route("/stream", methods=["GET"])
@require_admin
def stream_events():
    """Server-Sent Events stream of recent audit events."""
    after_id = int(request.args.get("after_id", 0))
    poll_iterations = 5
    poll_interval = 2

    def event_stream():
        session = get_session()
        nonlocal after_id
        try:
            for _ in range(poll_iterations):
                events = (
                    session.query(AuditEvent)
                    .filter(AuditEvent.id > after_id)
                    .order_by(AuditEvent.id.asc())
                    .limit(50)
                    .all()
                )
                if events:
                    for evt in events:
                        after_id = evt.id
                        yield _format_event(evt)
                yield "event: heartbeat\ndata: {}\n\n"
                time.sleep(poll_interval)
        finally:
            session.close()

    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")


@audit_bp.route("/events", methods=["GET"])
@require_admin
def list_events():
    """List recent audit events (non-stream)."""
    limit = min(int(request.args.get("limit", 100)), 500)
    session = get_session()
    events = (
        session.query(AuditEvent)
        .order_by(AuditEvent.created_at.desc())
        .limit(limit)
        .all()
    )
    session.close()
    return {
        "events": [
            {
                "id": evt.id,
                "event_type": evt.event_type,
                "payload": evt.payload,
                "signature_hash": evt.signature_hash,
                "created_at": evt.created_at.isoformat() if evt.created_at else None,
            }
            for evt in events
        ]
    }
