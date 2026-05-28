from sqlalchemy.orm import Session
from typing import Optional, List
from app.repositories.abstract.user import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class SQLUserRepository(UserRepository):
    """SQL implementation of User repository"""

    def __init__(self, db: Session):
        self.db = db

    def get(self, id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, obj: UserCreate) -> User:
        raise NotImplementedError("Use create_with_password instead")

    def create_with_password(self, email: str, full_name: str, hashed_password: str) -> User:
        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, id: int, obj_in: UserUpdate) -> Optional[User]:
        user = self.get(id)
        if not user:
            return None

        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(user, field, value)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, id: int) -> bool:
        user = self.get(id)
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True
