from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app.repositories.abstract.user import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class SQLUserRepository(UserRepository):
    """SQL implementation of User repository"""

    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    def create(self, obj: UserCreate) -> User:
        raise NotImplementedError(
            "Use create_user instead"
        )

    def create_user(self,
                    employee_id: str,
                    full_name: str,
                    email: str,
                    password_hash: str,
                    role: str,
                    designation: str | None = None) -> User:
        user = User(
            employee_id=employee_id,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role,
            designation=designation,
            status="active"
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_employee_id(self,
                           employee_id: str
    ) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.employee_id == employee_id)
            .first()
        )

    def update(self, id: UUID, obj_in: UserUpdate) -> Optional[User]:
        user = self.get(id)
        if not user:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(user, field, value)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, id: UUID) -> bool:
        user = self.get(id)
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True
