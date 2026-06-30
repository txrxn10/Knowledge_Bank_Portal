from app.models.tag import Tag
from app.schemas.tag import (
    TagCreate,
    TagUpdate
)
from app.repositories.abstract.tag import (
    TagRepository
)


class TagService:

    def __init__(
        self,
        tag_repo: TagRepository
    ):
        self.tag_repo = tag_repo

    def create_tag(
        self,
        tag_data: TagCreate
    ) -> Tag:

        existing_slug = (
            self.tag_repo.get_by_slug(
                tag_data.slug
            )
        )

        if existing_slug:
            raise ValueError(
                "Tag slug already exists"
            )

        return self.tag_repo.create_tag(
            name=tag_data.name,
            slug=tag_data.slug
        )

    def get_tag(
        self,
        tag_id
    ):
        return self.tag_repo.get(
            tag_id
        )

    def list_tags(
        self,
        skip: int = 0,
        limit: int = 100
    ):
        return self.tag_repo.get_all(
            skip,
            limit
        )

    def update_tag(
        self,
        tag_id,
        tag_data: TagUpdate
    ):
        return self.tag_repo.update(
            tag_id,
            tag_data
        )

    def delete_tag(
        self,
        tag_id
    ):
        return self.tag_repo.delete(
            tag_id
        )