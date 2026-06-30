from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse

)
from app.services.category import CategoryService
from app.dependencies import (
    get_category_service,
    get_category_repository
)

from app.repositories.abstract.category import (
    CategoryRepository
)
from app.core.exceptions import (
    NotFoundException,
    ConflictException
)

router = APIRouter(
    prefix="/categories",
    tags=["Master"]
)

@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category_in: CategoryCreate,
    category_service: CategoryService = Depends(
        get_category_service
    )
):
    try:
        return category_service.create_category(
            category_in
        )
    except ValueError as e:
        raise ConflictException(detail=str(e))


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: UUID,
    repo: CategoryRepository = Depends(
        get_category_repository
    )
):
    category = repo.get(category_id)

    if not category:
        raise NotFoundException(
            detail="Category not found"
        )

    return category


@router.get(
    "",
    response_model=list[CategoryResponse]
)
def list_categories(
    skip: int = 0,
    limit: int = 100,
    repo: CategoryRepository = Depends(
        get_category_repository
    )
):
    return repo.get_all(
        skip=skip,
        limit=limit
    )


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: UUID,
    category_in: CategoryUpdate,
    category_service: CategoryService = Depends(
        get_category_service
    )
):
    category = category_service.update_category(
        category_id,
        category_in
    )

    if not category:
        raise NotFoundException(
            detail="Category not found"
        )

    return category


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(
    category_id: UUID,
    category_service: CategoryService = Depends(
        get_category_service
    )
):
    deleted = category_service.delete_category(
        category_id
    )

    if not deleted:
        raise NotFoundException(
            detail="Category not found"
        )

    return None