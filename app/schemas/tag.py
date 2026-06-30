from pydantic import BaseModel
from uuid import UUID 
from datetime import datetime


class TageBase(BaseModel):
    name: str
    slug: str


class TagCreate(TageBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None

class TagResponse(TageBase):
    id: UUID

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True