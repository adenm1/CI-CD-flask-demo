"""Webhooks and third-party integration routes."""
from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timezone
from typing import Dict, Optional

from flask import Blueprint, current_app, jsonify, request

from backend.api.models import DeploymentLog, Pipeline
from backend.utils.db import get_session

integrations_bp = Blueprint("integrations", __name__, url_prefix="/api/integrations")


def _verify_signature(raw_body: bytes, signature_header: Optional[str]) -> bool:
    """Validate the GitHub HMAC signature."""
    secret = current_app.config.get("GITHUB_WEBHOOK_SECRET")
    if not secret:
        current_app.logger.warning("GITHUB_WEBHOOK_SECRET is not configured")
        return False

    if not signature_header or "=" not in signature_header:
        return False

    scheme, provided_signature = signature_header.split("=", 1)
    if scheme.lower() != "sha256":
        return False

    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(provided_signature, expected)


def _upsert_pipeline(payload: Dict[str, object]):
    """Create or update a pipeline record from webhook payload."""
    name = payload.get("name")
    if not name:
        raise ValueError("Pipeline name is required.")

    status = payload.get("status", "running")
    owner = payload.get("owner", "github-actions")
    run_id = payload.get("runId") or payload.get("run_id")

    session = get_session()
    try:
        if run_id:
            existing = session.query(Pipeline).filter(Pipeline.run_id == str(run_id)).first()
            if existing:
                existing.status = status
                existing.owner = owner
                existing.updated_at = datetime.now(timezone.utc)
                if status in ["success", "failed"]:
                    existing.completed_at = datetime.now(timezone.utc)
                    if existing.started_at:
                        duration = (existing.completed_at - existing.started_at).total_seconds() / 60
                        existing.duration_minutes = round(duration, 2)
                session.commit()
                session.refresh(existing)
                return existing

        pipeline = Pipeline(
            name=name,
            description=payload.get("description"),
            status=status,
            owner=owner,
            branch=payload.get("branch"),
            commit_sha=payload.get("commitSha"),
            commit_message=payload.get("commitMessage"),
            workflow_name=payload.get("workflowName"),
            run_id=str(run_id) if run_id else None,
            run_number=payload.get("runNumber"),
            started_at=datetime.now(timezone.utc),
        )

        if status in ["success", "failed"]:
            pipeline.completed_at = datetime.now(timezone.utc)
            pipeline.duration_minutes = payload.get("durationMinutes") or 0

        session.add(pipeline)
        session.commit()
        session.refresh(pipeline)

        log_level = (
            "success" if status == "success" else "error" if status == "failed" else "info"
        )
        log = DeploymentLog(
            pipeline_id=pipeline.id,
            level=log_level,
            message=f"Pipeline '{name}' {status}",
            timestamp=datetime.now(timezone.utc),
        )
        session.add(log)
        session.commit()
        return pipeline
    finally:
        session.close()


@integrations_bp.route("/github", methods=["POST"])
def github_pipeline():
    """Entry point for GitHub Actions to report pipeline status."""
    raw_body = request.get_data(cache=False)
    signature = request.headers.get("X-Hub-Signature-256")

    if not _verify_signature(raw_body, signature):
        return jsonify({"error": "Invalid webhook signature."}), 401

    payload = request.get_json(silent=True) or {}

    try:
        pipeline = _upsert_pipeline(payload)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:  # pragma: no cover - logged for observability
        current_app.logger.error("Failed to process pipeline payload: %s", exc, exc_info=True)
        return jsonify({"error": "Failed to process pipeline payload."}), 500

    return jsonify({"message": "Pipeline recorded", "pipeline": pipeline.to_dict()}), 201
