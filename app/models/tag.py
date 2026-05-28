from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class Tag(BaseModel):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
