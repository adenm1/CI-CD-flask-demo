"""Pipeline routes for CI/CD monitoring."""
from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy import desc

from backend.api.models import Pipeline, DeploymentLog
from backend.utils.db import get_session
from .decorators import require_admin

pipelines_bp = Blueprint("pipelines", __name__, url_prefix="/api/pipelines")


@pipelines_bp.route("", methods=["GET"])
@require_admin
def list_pipelines():
    """Get all pipelines with optional filtering."""
    session = get_session()

    # Get query parameters
    limit = request.args.get("limit", default=50, type=int)
    status = request.args.get("status")  # Filter by status

    query = session.query(Pipeline).order_by(desc(Pipeline.created_at))

    if status:
        query = query.filter(Pipeline.status == status)

    pipelines = query.limit(limit).all()

    return jsonify({
        "pipelines": [p.to_dict() for p in pipelines],
        "total": query.count()
    })


@pipelines_bp.route("", methods=["POST"])
@require_admin
def create_pipeline():
    """Create a new pipeline record (called by GitHub Actions)."""
    session = get_session()
    payload = request.get_json(silent=True) or {}

    # Extract data from payload
    name = payload.get("name")
    status = payload.get("status", "running")
    owner = payload.get("owner", "unknown")

    if not name:
        return jsonify({"error": "Pipeline name is required"}), 400

    # Check if pipeline with same run_id already exists (prevent duplicates)
    run_id = payload.get("runId")
    if run_id:
        existing = session.query(Pipeline).filter(Pipeline.run_id == run_id).first()
        if existing:
            # Update existing pipeline
            existing.status = status
            existing.updated_at = datetime.utcnow()

            if status in ["success", "failed"]:
                existing.completed_at = datetime.utcnow()
                if existing.started_at:
                    duration = (existing.completed_at - existing.started_at).total_seconds() / 60
                    existing.duration_minutes = round(duration, 2)

            session.commit()
            session.refresh(existing)

            return jsonify({
                "message": "Pipeline updated",
                "pipeline": existing.to_dict()
            })

    # Create new pipeline
    pipeline = Pipeline(
        name=name,
        description=payload.get("description"),
        status=status,
        owner=owner,
        branch=payload.get("branch"),
        commit_sha=payload.get("commitSha"),
        commit_message=payload.get("commitMessage"),
        workflow_name=payload.get("workflowName"),
        run_id=run_id,
        run_number=payload.get("runNumber"),
        started_at=datetime.utcnow()
    )

    # Set completion time if already completed
    if status in ["success", "failed"]:
        pipeline.completed_at = datetime.utcnow()
        pipeline.duration_minutes = payload.get("durationMinutes", 0)

    session.add(pipeline)
    session.commit()
    session.refresh(pipeline)

    # Create log entry
    log_level = "success" if status == "success" else "error" if status == "failed" else "info"
    log = DeploymentLog(
        pipeline_id=pipeline.id,
        level=log_level,
        message=f"Pipeline '{name}' {status}",
        timestamp=datetime.utcnow()
    )
    session.add(log)
    session.commit()

    return jsonify({
        "message": "Pipeline created successfully",
        "pipeline": pipeline.to_dict()
    }), 201


@pipelines_bp.route("/<int:pipeline_id>", methods=["GET"])
@require_admin
def get_pipeline(pipeline_id):
    """Get a single pipeline by ID."""
    session = get_session()
    pipeline = session.query(Pipeline).filter(Pipeline.id == pipeline_id).first()

    if not pipeline:
        return jsonify({"error": "Pipeline not found"}), 404

    return jsonify({"pipeline": pipeline.to_dict()})


@pipelines_bp.route("/stats", methods=["GET"])
@require_admin
def get_stats():
    """Get pipeline statistics."""
    session = get_session()

    total = session.query(Pipeline).count()
    successful = session.query(Pipeline).filter(Pipeline.status == "success").count()
    failed = session.query(Pipeline).filter(Pipeline.status == "failed").count()
    running = session.query(Pipeline).filter(Pipeline.status == "running").count()

    # Calculate average build time
    completed_pipelines = session.query(Pipeline).filter(
        Pipeline.status.in_(["success", "failed"]),
        Pipeline.duration_minutes.isnot(None)
    ).all()

    avg_build_time = 0
    if completed_pipelines:
        total_duration = sum(p.duration_minutes for p in completed_pipelines)
        avg_build_time = round(total_duration / len(completed_pipelines), 1)

    return jsonify({
        "total": total,
        "successful": successful,
        "failed": failed,
        "active": running,
        "avgBuildTime": avg_build_time
    })


@pipelines_bp.route("/logs", methods=["GET"])
@require_admin
def get_logs():
    """Get recent deployment logs."""
    session = get_session()

    limit = request.args.get("limit", default=50, type=int)
    logs = session.query(DeploymentLog).order_by(desc(DeploymentLog.timestamp)).limit(limit).all()

    return jsonify({
        "logs": [log.to_dict() for log in logs]
    })


@pipelines_bp.route("/history", methods=["GET"])
@require_admin
def get_history():
    """Get deployment history for charts (last 7 days)."""
    from datetime import timedelta
    from sqlalchemy import func

    session = get_session()

    # Get data from last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    # Group by date
    history_data = session.query(
        func.date(Pipeline.created_at).label('date'),
        func.sum(func.case((Pipeline.status == 'success', 1), else_=0)).label('successful'),
        func.sum(func.case((Pipeline.status == 'failed', 1), else_=0)).label('failed')
    ).filter(
        Pipeline.created_at >= seven_days_ago
    ).group_by(
        func.date(Pipeline.created_at)
    ).order_by('date').all()

    # Format response
    history = []
    for item in history_data:
        history.append({
            "date": item.date.isoformat(),
            "successful": int(item.successful or 0),
            "failed": int(item.failed or 0)
        })

    # Fill in missing days with zeros
    all_dates = []
    for i in range(7):
        date = (datetime.utcnow() - timedelta(days=6 - i)).date()
        all_dates.append(date)

    filled_history = []
    for date in all_dates:
        existing = next((h for h in history if h["date"] == date.isoformat()), None)
        if existing:
            filled_history.append(existing)
        else:
            filled_history.append({
                "date": date.isoformat(),
                "successful": 0,
                "failed": 0
            })

    return jsonify({"history": filled_history})
