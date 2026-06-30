from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)
from app.services.department import DepartmentService
from app.dependencies import (
    get_department_service,
    get_department_repository
)
from app.repositories.abstract.department import (
    DepartmentRepository
)
from app.core.exceptions import (
    NotFoundException,
    ConflictException
)

router = APIRouter(
    prefix="/departments",
    tags=["Master"]
)


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_department(
    department_in: DepartmentCreate,
    department_service: DepartmentService = Depends(
        get_department_service
    )
):
    try:
        return department_service.create_department(
            department_in
        )
    except ValueError as e:
        raise ConflictException(detail=str(e))


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_department(
    department_id: UUID,
    repo: DepartmentRepository = Depends(
        get_department_repository
    )
):
    department = repo.get(department_id)

    if not department:
        raise NotFoundException(
            detail="Department not found"
        )

    return department


@router.get(
    "",
    response_model=list[DepartmentResponse]
)
def list_departments(
    skip: int = 0,
    limit: int = 100,
    repo: DepartmentRepository = Depends(
        get_department_repository
    )
):
    return repo.get_all(
        skip=skip,
        limit=limit
    )


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_department(
    department_id: UUID,
    department_in: DepartmentUpdate,
    department_service: DepartmentService = Depends(
        get_department_service
    )
):
    department = department_service.update_department(
        department_id,
        department_in
    )

    if not department:
        raise NotFoundException(
            detail="Department not found"
        )

    return department


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_department(
    department_id: UUID,
    department_service: DepartmentService = Depends(
        get_department_service
    )
):
    deleted = department_service.delete_department(
        department_id
    )

    if not deleted:
        raise NotFoundException(
            detail="Department not found"
        )

    return None