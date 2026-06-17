from fastapi import APIRouter, Depends, status
from app.repositories.abstract.user import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.core.exceptions import NotFoundException, ConflictException
from app.services.user import UserService
from app.dependencies import get_user_service, get_user_repository
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/test", response_model=dict)
def test_domain():
    return {
        "success": True, 
        "message": "Test endpoint working", 
        "data": {"skip": 0, "limit": 100}
    }


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return user_service.create_user(user_in)
    except ValueError as e:
        raise ConflictException(detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
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

