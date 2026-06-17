from uuid import UUID
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.department import Department
from app.repositories.abstract.department import DepartmentRepository
from app.schemas.department import DepartmentUpdate


class SQLDepartmentRepository(DepartmentRepository):

    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[Department]:
        return (
            self.db.query(Department)
            .filter(Department.id == id)
            .first()
        )

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Department]:
        return (
            self.db.query(Department)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, obj):
        raise NotImplementedError(
            "Use create_department instead"
        )

    def get_by_slug(
        self,
        slug: str
    ) -> Optional[Department]:
        return (
            self.db.query(Department)
            .filter(Department.slug == slug)
            .first()
        )

    def create_department(
        self,
        name: str,
        slug: str,
        description: str | None = None,
        owner_id=None,
        parent_id=None,
        visibility: str = "internal"
    ) -> Department:

        department = Department(
            name=name,
            slug=slug,
            description=description,
            owner_id=owner_id,
            parent_id=parent_id,
            visibility=visibility,
            is_active=True
        )

        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)

        return department

    def update(
        self,
        id: UUID,
        obj_in: DepartmentUpdate
    ) -> Optional[Department]:

        department = self.get(id)

        if not department:
            return None

        update_data = obj_in.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(department, field, value)

        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)

        return department

    def delete(self, id: UUID) -> bool:

        department = self.get(id)

        if not department:
            return False

        self.db.delete(department)
        self.db.commit()

        return True