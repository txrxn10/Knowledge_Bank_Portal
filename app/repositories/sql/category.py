from uuid import UUID
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.abstract.category import CategoryRepository
from app.schemas.category import CategoryUpdate


class SQLCategoryRepository(CategoryRepository):

    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[Category]:
        return (
            self.db.query(Category)
            .filter(Category.id == id)
            .first()
        )

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Category]:
        return (
            self.db.query(Category)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, obj):
        raise NotImplementedError(
            "Use create_category instead"
        )

    def get_by_slug(
        self,
        slug: str
    ) -> Optional[Category]:
        return (
            self.db.query(Category)
            .filter(Category.slug == slug)
            .first()
        )

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

        category = Category(
            name=name,
            slug=slug,
            description=description,
            owner_id=owner_id,
            parent_id=parent_id,
            icon_url=icon_url,
            sort_order=sort_order,
            is_active=True
        )

        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    def update(
        self,
        id: UUID,
        obj_in: CategoryUpdate
    ) -> Optional[Category]:

        category = self.get(id)

        if not category:
            return None

        update_data = obj_in.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(category, field, value)

        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    def delete(self, id: UUID) -> bool:

        category = self.get(id)

        if not category:
            return False

        self.db.delete(category)
        self.db.commit()

        return True