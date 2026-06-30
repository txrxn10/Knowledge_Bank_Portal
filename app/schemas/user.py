from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

from app.constants.roles import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    employee_id: str
    password: str

    role: UserRole

    designation: str | None = None
    department_id: UUID | None = None
    reporting_manager: UUID | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None

    role: UserRole | None = None
    designation: str | None = None

    department_id: UUID | None = None
    reporting_manager: UUID | None = None

    status: str | None = None


class UserResponse(UserBase):
    id: UUID
    employee_id: str | None
    role: str
    status: str
    designation: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True