from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.utils.security import decode_access_token


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


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_access_token(token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_repo = SQLUserRepository(db)

    user = user_repo.get(user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user