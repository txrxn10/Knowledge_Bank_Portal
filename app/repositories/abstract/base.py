from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

from sqlalchemy import UUID

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository for data access operations"""

    @abstractmethod
    def get(self, id: UUID) -> Optional[T]:
        """Get a single item by ID"""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all items with pagination"""
        pass

    @abstractmethod
    def create(self, obj: T) -> T:
        """Create a new item"""
        pass

    @abstractmethod
    def update(self, id: UUID, obj_in) -> Optional[T]:
        """Update an existing item"""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        """Delete an item by ID"""
        pass

