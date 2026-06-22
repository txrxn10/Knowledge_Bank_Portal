from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.sql.user import SQLUserRepository
from app.services.auth import AuthService
from app.schemas.auth import LoginRequest, TokenResponse
from app.dependencies import get_current_user
from app.models.user import User



router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    auth_service = AuthService(
        user_repo=SQLUserRepository(db)
    )

    try:
        return auth_service.login(
            login_data.email,
            login_data.password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role
    }

