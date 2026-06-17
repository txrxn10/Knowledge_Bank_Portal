from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class DepartmentBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    visibility: str = "internal"



class DepartmentCreate(DepartmentBase):
    owner_id: UUID | None = None
    parent_id: UUID | None = None


class DepartmentUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    visibility: str | None = None
    owner_id: UUID | None = None
    parent_id: UUID | None= None
    is_active: bool | None = None



class DepartmentResponse(DepartmentBase):
    id: UUID
    owner_id: UUID | None
    parent_id: UUID | None
    is_active: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True