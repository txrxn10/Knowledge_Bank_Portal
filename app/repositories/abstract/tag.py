from abc import abstractmethod
from typing import Optional

from app.models.tag import Tag
from app.repositories.abstract.base import BaseRepository


class TagRepository(BaseRepository[Tag]):

    @abstractmethod
    def get_by_slug(
        self,
        slug: str
    ) -> Optional[Tag]:
        pass

    @abstractmethod
    def create_tag(
        self,
        name: str,
        slug: str
    ) -> Tag:
        pass