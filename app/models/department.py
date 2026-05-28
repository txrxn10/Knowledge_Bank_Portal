from sqlalchemy import Column, String, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class Department(BaseModel):
    __tablename__ = "departments"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name            = Column(String(150), nullable=False)
    slug            = Column(String(150), nullable=False)
    description     = Column(String, nullable=True)
    owner_id        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    visibility      = Column(String(10), nullable=False)
    is_active       = Column(Boolean, default=True)
    parent_id       = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    dept_metadata   = Column(JSON, nullable=True)
    deleted_at      = Column(String, nullable=True)


class DepartmentCategory(BaseModel):
    __tablename__   = "department_categories"
    __table_args__  = {"extend_existing": True}

    department_id   = Column(UUID(as_uuid=True), ForeignKey("departments.id"), primary_key=True)
    category_id     = Column(UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=True)
    is_primary      = Column(Boolean, default=False)
    mapped_by       = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    mapped_at       = Column(String, nullable=True)


class UserDepartment(BaseModel):
    __tablename__   = "user_departments"
    __table_args__  = {"extend_existing": True}

    user_id         = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    department_id   = Column(UUID(as_uuid=True), ForeignKey("departments.id"), primary_key=True)
    role_override   = Column(String(11), nullable=True)
    joined_at       = Column(String, nullable=True)
