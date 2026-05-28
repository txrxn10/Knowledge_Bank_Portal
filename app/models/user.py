from sqlalchemy import Column, String, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class User(BaseModel):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(String(50), nullable=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(11), nullable=False)
    status = Column(String(9), nullable=False, default="active")
    designation = Column(String(150), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    reporting_manager = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    last_login_at = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)
    deleted_at = Column(String, nullable=True)
