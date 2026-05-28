from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.db.base import BaseModel
import uuid


class SharedLink(BaseModel):
    __tablename__ = "shared_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    shared_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    scope = Column(String(13), nullable=False)
    access_level = Column(String(8), nullable=False)
    shared_with_user = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    shared_with_dept = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    token = Column(String, nullable=True)
    token_hash = Column(String(64), nullable=True)
    guest_email = Column(String(255), nullable=True)
    guest_name = Column(String(200), nullable=True)
    password_hash = Column(String, nullable=True)
    expires_at = Column(String, nullable=True)
    max_views = Column(Integer, nullable=True)
    max_downloads = Column(Integer, nullable=True)
    allowed_domains = Column(ARRAY(String), nullable=True)
    watermark_enabled = Column(Boolean, default=False)
    download_allowed = Column(Boolean, default=True)
    print_allowed = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    revoked_at = Column(String, nullable=True)
    revoked_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
