from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional

from app.models.collection import Collection
from app.schemas.collection import CollectionUpdate


class CollectionRepository(ABC):

    @abstractmethod
    def get(self, id: UUID) -> Optional[Collection]:
        pass

    @abstractmethod
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Collection]:
        pass

    @abstractmethod
    def create_collection(
        self,
        name: str,
        description: str | None
    ) -> Collection:
        pass

    @abstractmethod
    def update(
        self,
        id: UUID,
        obj_in: CollectionUpdate
    ) -> Optional[Collection]:
        pass

    @abstractmethod
    def delete(
        self,
        id: UUID
    ) -> bool:
        pass