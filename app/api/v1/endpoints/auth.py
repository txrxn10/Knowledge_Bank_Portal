from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.sql.user import SQLUserRepository
from app.services.auth import AuthService
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.dependencies import get_current_user
from app.models.user import User



router = APIRouter(
    prefix="/auth",
    tags = ["auth"]

)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    auth_service = AuthService(
        user_repo=SQLUserRepository(db)
    )

    try:
        return auth_service.login(
            form_data.username,
            form_data.password
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    


@router.post("/refresh")
def refresh_token(
    request: RefreshTokenRequest

):
    from app.utils.security import decode_refresh_token
    from app.utils.security import create_access_token

    user_id = decode_refresh_token(
        request.refresh_token
    )

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    
    access_token = create_access_token(
        {"sub": str(user_id)}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


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






