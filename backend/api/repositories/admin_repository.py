"""Admin user repository."""
from typing import Optional
from backend.api.models import AdminUser
from backend.api.repositories.base import BaseRepository


class AdminRepository(BaseRepository[AdminUser]):
    """Repository for AdminUser model."""

    def __init__(self):
        super().__init__(AdminUser)

    def get_by_username(self, username: str) -> Optional[AdminUser]:
        """Get admin by username.

        Args:
            username: Admin username

        Returns:
            AdminUser or None
        """
        return self.get_one(username=username)

    def get_active_admins(self):
        """Get all active admins.

        Returns:
            List of active AdminUser instances
        """
        return self.get_all(is_active=True)

    def username_exists(self, username: str) -> bool:
        """Check if username exists.

        Args:
            username: Username to check

        Returns:
            True if username exists
        """
        return self.exists(username=username)
