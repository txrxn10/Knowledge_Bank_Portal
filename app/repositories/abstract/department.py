from abc import abstractmethod
from typing import Optional

from app.models.department import Department
from app.repositories.abstract.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):

    @abstractmethod
    def get_by_slug(
        self,
        slug: str
    ) -> Optional[Department]:
        pass

    @abstractmethod
    def create_department(
        self,
        name: str,
        slug: str,
        description: str | None = None,
        owner_id=None,
        parent_id=None,
        visibility: str = "internal"
    ) -> Department:
        pass