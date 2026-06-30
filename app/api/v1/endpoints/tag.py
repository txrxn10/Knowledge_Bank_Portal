from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.schemas.tag import (
    TagCreate,
    TagUpdate,
    TagResponse
)

from app.services.tag import TagService

from app.dependencies import (
    get_tag_service,
    get_tag_repository
)

from app.repositories.abstract.tag import (
    TagRepository
)

from app.core.exceptions import (
    NotFoundException,
    ConflictException
)

router = APIRouter(
    prefix="/tags",
    tags=["Master - Tags"]
)


@router.post(
    "",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED
)
def create_tag(
    tag_in: TagCreate,
    tag_service: TagService = Depends(
        get_tag_service
    )
):
    try:
        return tag_service.create_tag(
            tag_in
        )
    except ValueError as e:
        raise ConflictException(
            detail=str(e)
        )
    

@router.get(
    "/{tag_id}",
    response_model=TagResponse
)
def get_tag(
    tag_id: UUID,
    repo: TagRepository = Depends(
        get_tag_repository
    )
):
    tag = repo.get(tag_id)

    if not tag:
        raise NotFoundException(
            detail="Tag not found"
        )

    return tag




@router.get(
    "",
    response_model=list[TagResponse]
)
def list_tags(
    skip: int = 0,
    limit: int = 100,
    repo: TagRepository = Depends(
        get_tag_repository
    )
):
    return repo.get_all(
        skip=skip,
        limit=limit
    )



@router.put(
    "/{tag_id}",
    response_model=TagResponse
)
def update_tag(
    tag_id: UUID,
    tag_in: TagUpdate,
    tag_service: TagService = Depends(
        get_tag_service
    )
):
    tag = tag_service.update_tag(
        tag_id,
        tag_in
    )

    if not tag:
        raise NotFoundException(
            detail="Tag not found"
        )

    return tag



@router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_tag(
    tag_id: UUID,
    tag_service: TagService = Depends(
        get_tag_service
    )
):
    deleted = tag_service.delete_tag(
        tag_id
    )

    if not deleted:
        raise NotFoundException(
            detail="Tag not found"
        )

    return None