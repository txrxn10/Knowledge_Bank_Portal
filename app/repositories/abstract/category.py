from abc import abstractmethod
from typing import Optional

from app.models.category import Category
from app.repositories.abstract.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):

    @abstractmethod
    def get_by_slug(
        self,
        slug: str
    ) -> Optional[Category]:
        pass

    @abstractmethod
    def create_category(
        self,
        name: str,
        slug: str,
        description: str | None = None,
        owner_id=None,
        parent_id=None,
        icon_url: str | None = None,
        sort_order: int | None = None
    ) -> Category:
        pass