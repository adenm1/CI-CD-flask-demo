"""Base repository pattern for database operations."""
from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from backend.utils.db import get_session

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Base repository providing common database operations."""

    def __init__(self, model: Type[T], session: Optional[Session] = None):
        """Initialize repository.

        Args:
            model: SQLAlchemy model class
            session: Optional SQLAlchemy session (will create new one if not provided)
        """
        self.model = model
        self._session = session

    @property
    def session(self) -> Session:
        """Get or create session."""
        if self._session is None:
            self._session = get_session()
        return self._session

    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID.

        Args:
            id: Entity ID

        Returns:
            Entity or None if not found
        """
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self, **filters) -> List[T]:
        """Get all entities matching filters.

        Args:
            **filters: Field=value filters

        Returns:
            List of entities
        """
        query = self.session.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.all()

    def get_one(self, **filters) -> Optional[T]:
        """Get single entity matching filters.

        Args:
            **filters: Field=value filters

        Returns:
            Entity or None
        """
        query = self.session.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first()

    def create(self, **kwargs) -> T:
        """Create new entity.

        Args:
            **kwargs: Entity fields

        Returns:
            Created entity
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def update(self, entity: T, **kwargs) -> T:
        """Update entity fields.

        Args:
            entity: Entity to update
            **kwargs: Fields to update

        Returns:
            Updated entity
        """
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        """Delete entity.

        Args:
            entity: Entity to delete
        """
        self.session.delete(entity)
        self.session.commit()

    def count(self, **filters) -> int:
        """Count entities matching filters.

        Args:
            **filters: Field=value filters

        Returns:
            Count of entities
        """
        query = self.session.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.count()

    def exists(self, **filters) -> bool:
        """Check if entity exists.

        Args:
            **filters: Field=value filters

        Returns:
            True if exists
        """
        return self.count(**filters) > 0
