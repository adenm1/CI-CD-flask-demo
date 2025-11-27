"""Pipeline repository."""
from typing import List, Optional
from datetime import datetime, timedelta
from backend.api.models import Pipeline
from backend.api.repositories.base import BaseRepository


class PipelineRepository(BaseRepository[Pipeline]):
    """Repository for Pipeline model."""

    def __init__(self):
        super().__init__(Pipeline)

    def get_by_status(self, status: str) -> List[Pipeline]:
        """Get pipelines by status.

        Args:
            status: Pipeline status

        Returns:
            List of pipelines
        """
        return self.get_all(status=status)

    def get_recent(self, limit: int = 10) -> List[Pipeline]:
        """Get most recent pipelines.

        Args:
            limit: Number of pipelines to return

        Returns:
            List of recent pipelines
        """
        return (
            self.session.query(Pipeline)
            .order_by(Pipeline.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_owner(self, owner: str) -> List[Pipeline]:
        """Get pipelines by owner.

        Args:
            owner: Owner name

        Returns:
            List of pipelines
        """
        return self.get_all(owner=owner)

    def get_statistics(self) -> dict:
        """Get pipeline statistics.

        Returns:
            Dictionary with statistics
        """
        total = self.count()
        successful = self.count(status='success')
        failed = self.count(status='failed')
        running = self.count(status='running')

        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'running': running,
            'success_rate': (successful / total * 100) if total > 0 else 0
        }
