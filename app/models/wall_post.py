from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class WallPost(BaseModel):
    __tablename__ = "wall_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    is_pinned = Column(Boolean, default=False)
    pinned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    pinned_at = Column(String, nullable=True)
    attachment_url = Column(String, nullable=True)
    attachment_type = Column(String(12), nullable=True)
    visibility = Column(String(10), nullable=False)
    deleted_at = Column(String, nullable=True)
