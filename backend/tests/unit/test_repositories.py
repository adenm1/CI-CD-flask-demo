"""Unit tests for repository pattern."""
import pytest
from backend.api.repositories import AdminRepository, PipelineRepository
from backend.tests.factories import AdminUserFactory, PipelineFactory


class TestAdminRepository:
    """Test AdminRepository."""

    def test_get_by_username(self, app):
        """Test getting admin by username."""
        repo = AdminRepository()
        admin = repo.create(username="testuser", password_hash="hash123")

        found = repo.get_by_username("testuser")
        assert found is not None
        assert found.username == "testuser"

    def test_username_exists(self, app):
        """Test checking if username exists."""
        repo = AdminRepository()
        repo.create(username="exists", password_hash="hash123")

        assert repo.username_exists("exists") is True
        assert repo.username_exists("nonexistent") is False

    def test_get_active_admins(self, app):
        """Test getting active admins."""
        repo = AdminRepository()
        repo.create(username="active1", password_hash="hash1", is_active=True)
        repo.create(username="active2", password_hash="hash2", is_active=True)
        repo.create(username="inactive", password_hash="hash3", is_active=False)

        active = repo.get_active_admins()
        # Default admin + 2 created = 3
        assert len([a for a in active if a.username in ['active1', 'active2']]) == 2


class TestPipelineRepository:
    """Test PipelineRepository."""

    def test_get_by_status(self, app):
        """Test getting pipelines by status."""
        from backend.utils.db import get_session
        from backend.api.models import Pipeline

        session = get_session()
        p1 = Pipeline(name="test1", status="success", owner="testuser")
        p2 = Pipeline(name="test2", status="failed", owner="testuser")
        session.add_all([p1, p2])
        session.commit()

        repo = PipelineRepository()
        success_pipes = repo.get_by_status("success")

        assert len(success_pipes) >= 1
        assert any(p.name == "test1" for p in success_pipes)

    def test_get_statistics(self, app):
        """Test getting pipeline statistics."""
        from backend.utils.db import get_session
        from backend.api.models import Pipeline

        session = get_session()
        session.add_all([
            Pipeline(name="p1", status="success", owner="testuser"),
            Pipeline(name="p2", status="success", owner="testuser"),
            Pipeline(name="p3", status="failed", owner="testuser"),
        ])
        session.commit()

        repo = PipelineRepository()
        stats = repo.get_statistics()

        assert stats['total'] == 3
        assert stats['successful'] == 2
        assert stats['failed'] == 1
        assert stats['success_rate'] > 0
