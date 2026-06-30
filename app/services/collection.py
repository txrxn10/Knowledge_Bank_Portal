from uuid import UUID
from typing import List

from app.models.collection import Collection
from app.schemas.collection import CollectionCreate, CollectionUpdate
from app.repositories.abstract.collection import CollectionRepository


class CollectionService:

    def __init__(
        self,
        collection_repo: CollectionRepository
    ):
        self.collection_repo = collection_repo

    def create_collection(
        self,
        collection_in: CollectionCreate
    ) -> Collection:

        existing = self.collection_repo.get_by_slug(
            collection_in.slug
        )

        if existing:
            raise ValueError(
                "Collection slug already exists"
            )

        return self.collection_repo.create_collection(
            name=collection_in.name,
            slug=collection_in.slug,
            description=collection_in.description,
            department_id=collection_in.department_id,
            owner_id=collection_in.owner_id,
            is_public=collection_in.is_public
        )

    def get_collection(
        self,
        collection_id: UUID
    ):
        return self.collection_repo.get(collection_id)

    def list_collections(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Collection]:
        return self.collection_repo.get_all(
            skip,
            limit
        )

    def update_collection(
        self,
        collection_id: UUID,
        collection_in: CollectionUpdate
    ):
        return self.collection_repo.update(
            collection_id,
            collection_in
        )

    def delete_collection(
        self,
        collection_id: UUID
    ) -> bool:
        return self.collection_repo.delete(
            collection_id
        )