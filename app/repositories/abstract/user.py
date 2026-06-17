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
    def create_user(
                    self, 
                    employee_id: str,
                    full_name: str,
                    email: str,
                    role: str,
                    designation: str | None = None,
    )-> User:
        pass

    @abstractmethod
    def get_by_employee_id(self, employee_id: str) -> Optional[User]:
        """Get user by employee ID"""
        pass
