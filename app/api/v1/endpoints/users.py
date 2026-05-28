from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.repositories.abstract.user import UserRepository
from app.dependencies import get_user_repository
from app.core.exceptions import NotFoundException, ConflictException
from app.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/test", response_model=dict)
def test_domain():
    return {
        "success": True, 
        "message": "Test endpoint working", 
        "data": {"skip": 0, "limit": 100}
    }


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    repo: UserRepository = Depends(get_user_repository)
):
    existing_user = repo.get_by_email(user_in.email)
    if existing_user:
        raise ConflictException(detail="Email already registered")

    hashed_password = hash_password(user_in.password)
    user = repo.create_with_password(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password
    )
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository)
):
    user = repo.get(user_id)
    if not user:
        raise NotFoundException(detail="User not found")
    return user


@router.get("", response_model=list[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    repo: UserRepository = Depends(get_user_repository)
):
    return repo.get_all(skip=skip, limit=limit)

