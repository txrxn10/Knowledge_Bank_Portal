from uuid import UUID
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.collection import Collection
from app.repositories.abstract.collection import CollectionRepository
from app.schemas.collection import CollectionUpdate


class SQLCollectionRepository(CollectionRepository):

    def __init__(self, db: Session):
        self.db = db

    def get(
        self,
        id: UUID
    ) -> Optional[Collection]:
        return (
            self.db.query(Collection)
            .filter(Collection.id == id)
            .first()
        )

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Collection]:
        return (
            self.db.query(Collection)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_slug(
        self,
        slug: str
    ) -> Optional[Collection]:
        return (
            self.db.query(Collection)
            .filter(Collection.slug == slug)
            .first()
        )

    def create_collection(
        self,
        name: str,
        slug: str,
        description: str | None,
        department_id: UUID | None,
        owner_id: UUID | None,
        is_public: bool
    ) -> Collection:

        collection = Collection(
            name=name,
            slug=slug,
            description=description,
            department_id=department_id,
            owner_id=owner_id,
            is_public=is_public
        )

        self.db.add(collection)
        self.db.commit()
        self.db.refresh(collection)

        return collection

    def update(
        self,
        id: UUID,
        obj_in: CollectionUpdate
    ) -> Optional[Collection]:

        collection = self.get(id)

        if not collection:
            return None

        update_data = obj_in.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(collection, field, value)

        self.db.add(collection)
        self.db.commit()
        self.db.refresh(collection)

        return collection

    def delete(
        self,
        id: UUID
    ) -> bool:

        collection = self.get(id)

        if not collection:
            return False

        self.db.delete(collection)
        self.db.commit()

        return True