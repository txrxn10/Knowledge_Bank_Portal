from sqlalchemy import Column, String, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class Achievement(BaseModel):
    __tablename__ = "achievements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    description = Column(String, nullable=True)
    type = Column(String(19), nullable=False)
    badge_url = Column(String, nullable=True)
    criteria = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)


class UserAchievement(BaseModel):
    __tablename__ = "user_achievements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    achievement_id = Column(UUID(as_uuid=True), ForeignKey("achievements.id"), nullable=False)
    awarded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    award_period = Column(String(20), nullable=True)
    notes = Column(String, nullable=True)
    awarded_at = Column(String, nullable=True)
