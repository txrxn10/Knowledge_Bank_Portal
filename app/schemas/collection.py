from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CollectionCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    department_id: Optional[UUID] = None
    owner_id: Optional[UUID] = None
    is_public: bool = False


class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[UUID] = None
    owner_id: Optional[UUID] = None
    is_public: Optional[bool] = None


class CollectionResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    department_id: Optional[UUID]
    owner_id: Optional[UUID]
    is_public: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )