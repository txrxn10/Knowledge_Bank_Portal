from app.models.category import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate
)
from app.repositories.abstract.category import (
    CategoryRepository
)


class CategoryService:

    def __init__(
        self,
        category_repo: CategoryRepository
    ):
        self.category_repo = category_repo

    def create_category(
        self,
        category_data: CategoryCreate
    ) -> Category:

        existing_slug = (
            self.category_repo.get_by_slug(
                category_data.slug
            )
        )

        if existing_slug:
            raise ValueError(
                "Category slug already exists"
            )

        return self.category_repo.create_category(
            name=category_data.name,
            slug=category_data.slug,
            description=category_data.description,
            owner_id=category_data.owner_id,
            parent_id=category_data.parent_id,
            icon_url=category_data.icon_url,
            sort_order=category_data.sort_order
        )

    def get_category(
        self,
        category_id
    ):
        return self.category_repo.get(
            category_id
        )

    def list_categories(
        self,
        skip: int = 0,
        limit: int = 100
    ):
        return self.category_repo.get_all(
            skip,
            limit
        )

    def update_category(
        self,
        category_id,
        category_data: CategoryUpdate
    ):
        return self.category_repo.update(
            category_id,
            category_data
        )

    def delete_category(
        self,
        category_id
    ):
        return self.category_repo.delete(
            category_id
        )