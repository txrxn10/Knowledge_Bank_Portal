from sqlalchemy import Column, String, Boolean, Integer, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY, TSVECTOR
from app.db.base import BaseModel
import uuid


class Resource(BaseModel):
    __tablename__ = "resources"

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title               = Column(String(300), nullable=False)
    slug                = Column(String(300), nullable=False)
    description         = Column(String, nullable=True)
    summary             = Column(String, nullable=True)
    resource_type       = Column(String(12), nullable=False)
    category_id         = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    department_id       = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    visibility          = Column(String(10), nullable=False)
    approval_status     = Column(String(14), nullable=False)
    file_url            = Column(String, nullable=True)
    file_size_bytes     = Column(BigInteger, nullable=True)
    file_mime_type      = Column(String(100), nullable=True)
    youtube_url         = Column(String, nullable=True)
    thumbnail_url       = Column(String, nullable=True)
    duration_seconds    = Column(Integer, nullable=True)
    keywords            = Column(ARRAY(String), nullable=True)
    is_featured         = Column(Boolean, default=False)
    version             = Column(String(20), nullable=True)
    expires_at          = Column(String, nullable=True)
    uploaded_by         = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_by         = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at         = Column(String, nullable=True)
    ai_title_used       = Column(Boolean, default=False)
    ai_desc_used        = Column(Boolean, default=False)
    ai_tags_used        = Column(Boolean, default=False)
    ai_summary_used     = Column(Boolean, default=False)
    view_count          = Column(BigInteger, default=0)
    download_count      = Column(BigInteger, default=0)
    search_vector       = Column(TSVECTOR, nullable=True)
    published_at        = Column(String, nullable=True)
    deleted_at          = Column(String, nullable=True)


class ResourceTag(BaseModel):
    __tablename__ = "resource_tags"
    __table_args__ = {"extend_existing": True}

    resource_id     = Column(UUID(as_uuid=True), ForeignKey("resources.id"), primary_key=True)
    tag_id          = Column(UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True)
    added_by_ai     = Column(Boolean, default=False)


class ResourceVersion(BaseModel):
    __tablename__ = "resource_versions"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id     = Column(UUID(as_uuid=True), ForeignKey("resources.id"), nullable=False)
    version         = Column(String(20), nullable=False)
    change_summary  = Column(String, nullable=True)
    file_url        = Column(String, nullable=True)
    file_size_bytes = Column(BigInteger, nullable=True)
    created_by      = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
