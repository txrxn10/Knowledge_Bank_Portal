from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class Permission(BaseModel):
    __tablename__ = "permissions"

    id                = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id           = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    resource_type     = Column(String(50), nullable=False)
    resource_id       = Column(UUID(as_uuid=True), nullable=True)
    can_view          = Column(Boolean, default=False)
    can_upload        = Column(Boolean, default=False)
    can_edit          = Column(Boolean, default=False)
    can_delete        = Column(Boolean, default=False)
    can_approve       = Column(Boolean, default=False)
    can_manage        = Column(Boolean, default=False)
    granted_by        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    expires_at        = Column(String, nullable=True)
