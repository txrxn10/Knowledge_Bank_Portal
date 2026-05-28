from sqlalchemy import Column, String, Boolean, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class Category(BaseModel):
    __tablename__   = "categories"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name            = Column(String(150), nullable=False)
    slug            = Column(String(150), nullable=False)
    description     = Column(String, nullable=True)
    owner_id        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    parent_id       = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    icon_url        = Column(String, nullable=True)
    is_active       = Column(Boolean, default=True)
    sort_order      = Column(Integer, nullable=True)
    cat_metadata    = Column(JSON, nullable=True)
    deleted_at      = Column(String, nullable=True)
