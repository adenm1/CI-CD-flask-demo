"""Pipeline model for storing CI/CD pipeline data."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from backend.utils.db import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Pipeline(Base):
    """Pipeline deployment record."""

    __tablename__ = 'pipelines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default='queued')  # queued, running, success, failed
    owner = Column(String(100), nullable=False)

    # Timing information
    started_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_minutes = Column(Float, nullable=True)

    # Metadata
    branch = Column(String(100), nullable=True)
    commit_sha = Column(String(40), nullable=True)
    commit_message = Column(Text, nullable=True)

    # GitHub Actions specific
    workflow_name = Column(String(255), nullable=True)
    run_id = Column(String(100), nullable=True, unique=True)
    run_number = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)

    def __repr__(self):
        return f'<Pipeline {self.name} - {self.status}>'

    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'owner': self.owner,
            'startedAt': self.started_at.isoformat() if self.started_at else None,
            'completedAt': self.completed_at.isoformat() if self.completed_at else None,
            'durationMinutes': self.duration_minutes,
            'branch': self.branch,
            'commitSha': self.commit_sha,
            'commitMessage': self.commit_message,
            'workflowName': self.workflow_name,
            'runId': self.run_id,
            'runNumber': self.run_number,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }


class DeploymentLog(Base):
    """Deployment log entry."""

    __tablename__ = 'deployment_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pipeline_id = Column(Integer, nullable=True)  # Can be null for system logs
    level = Column(String(20), nullable=False, default='info')  # info, warning, error, success
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=_utcnow)

    def __repr__(self):
        return f'<DeploymentLog {self.level}: {self.message[:50]}>'

    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'pipelineId': self.pipeline_id,
            'level': self.level,
            'message': self.message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
