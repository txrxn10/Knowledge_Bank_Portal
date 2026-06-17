from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.user import UserService
from app.services.department import DepartmentService

from app.repositories.sql.user import SQLUserRepository
from app.repositories.sql.department import SQLDepartmentRepository

from app.repositories.abstract.user import UserRepository
from app.repositories.abstract.department import DepartmentRepository


def get_user_repository(
    db: Session = Depends(get_db)
) -> UserRepository:
    return SQLUserRepository(db)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repo)


def get_department_repository(
    db: Session = Depends(get_db)
) -> DepartmentRepository:
    return SQLDepartmentRepository(db)


def get_department_service(
    repo: DepartmentRepository = Depends(
        get_department_repository
    )
) -> DepartmentService:
    return DepartmentService(repo)