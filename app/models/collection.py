from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class Collection(BaseModel):
    __tablename__ = "collections"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name            = Column(String(200), nullable=False)
    slug            = Column(String(200), nullable=False)
    description     = Column(String, nullable=True)
    department_id   = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    owner_id        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_public       = Column(Boolean, default=False)


class CollectionDocument(BaseModel):
    __tablename__   = "collection_documents"
    __table_args__  = {"extend_existing": True}

    collection_id   = Column(UUID(as_uuid=True), ForeignKey("collections.id"), primary_key=True)
    document_id     = Column(UUID(as_uuid=True), ForeignKey("documents.id"), primary_key=True)
    sort_order      = Column(Integer, nullable=True)
    added_by        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    added_at        = Column(String, nullable=True)
