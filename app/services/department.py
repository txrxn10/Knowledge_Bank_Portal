from app.models.department import Department
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate
)
from app.repositories.abstract.department import (
    DepartmentRepository
)


class DepartmentService:

    def __init__(
        self,
        department_repo: DepartmentRepository
    ):
        self.department_repo = department_repo

    def create_department(
        self,
        department_data: DepartmentCreate
    ) -> Department:

        existing_slug = (
            self.department_repo.get_by_slug(
                department_data.slug
            )
        )

        if existing_slug:
            raise ValueError(
                "Department slug already exists"
            )

        return self.department_repo.create_department(
            name=department_data.name,
            slug=department_data.slug,
            description=department_data.description,
            owner_id=department_data.owner_id,
            parent_id=department_data.parent_id,
            visibility=department_data.visibility
        )

    def get_department(
        self,
        department_id
    ):
        return self.department_repo.get(
            department_id
        )

    def list_departments(
        self,
        skip: int = 0,
        limit: int = 100
    ):
        return self.department_repo.get_all(
            skip,
            limit
        )

    def update_department(
        self,
        department_id,
        department_data: DepartmentUpdate
    ):
        return self.department_repo.update(
            department_id,
            department_data
        )

    def delete_department(
        self,
        department_id
    ):
        return self.department_repo.delete(
            department_id
        )