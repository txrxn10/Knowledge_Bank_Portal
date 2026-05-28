from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, INET
from app.db.base import BaseModel
import uuid


class Session(BaseModel):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    token_hash = Column(String, nullable=False)
    ip_address = Column(INET, nullable=True)
    user_agent = Column(String, nullable=True)
    expires_at = Column(String, nullable=False)
    revoked_at = Column(String, nullable=True)
