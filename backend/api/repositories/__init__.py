"""Repository pattern for database access."""
from .base import BaseRepository
from .admin_repository import AdminRepository
from .pipeline_repository import PipelineRepository

__all__ = ['BaseRepository', 'AdminRepository', 'PipelineRepository']
