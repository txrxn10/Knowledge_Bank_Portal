from abc import abstractmethod
from typing import Optional
from app.repositories.abstract.base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository[User]):
    """Abstract User repository"""

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass

    @abstractmethod
    def create_with_password(self, email: str, full_name: str, hashed_password: str) -> User:
        """Create user with hashed password"""
        pass
