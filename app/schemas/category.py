from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    owner_id: UUID | None = None
    parent_id: UUID | None = None
    icon_url: str | None = None
    sort_order: int | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    owner_id: UUID | None = None
    parent_id: UUID | None = None
    icon_url: str | None = None
    sort_order: int | None = None
    is_active: bool | None = None


class CategoryResponse(CategoryBase):
    id: UUID
    owner_id: UUID | None
    parent_id: UUID | None
    icon_url: str | None
    sort_order: int | None
    is_active: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True