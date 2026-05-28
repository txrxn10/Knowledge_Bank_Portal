from sqlalchemy import Column, String, Boolean, Integer, BigInteger, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY, TSVECTOR
from app.db.base import BaseModel
import uuid


class Document(BaseModel):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(400), nullable=False)
    slug = Column(String(400), nullable=False)
    description = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    format = Column(String(5), nullable=False)
    status = Column(String(12), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    visibility = Column(String(10), nullable=False)
    storage_bucket = Column(String(100), nullable=True)
    storage_key = Column(String, nullable=True)
    file_url = Column(String, nullable=True)
    file_size_bytes = Column(BigInteger, nullable=True)
    file_mime_type = Column(String(100), nullable=True)
    checksum_sha256 = Column(String(64), nullable=True)
    is_encrypted = Column(Boolean, default=False)
    external_url = Column(String, nullable=True)
    is_external_link = Column(Boolean, default=False)
    thumbnail_url = Column(String, nullable=True)
    preview_pages = Column(JSON, nullable=True)
    keywords = Column(ARRAY(String), nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    language = Column(String(10), nullable=True)
    page_count = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    is_featured = Column(Boolean, default=False)
    expires_at = Column(String, nullable=True)
    version = Column(String(20), nullable=True)
    version_notes = Column(String, nullable=True)
    parent_doc_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    is_latest_version = Column(Boolean, default=True)
    approval_status = Column(String(14), nullable=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(String, nullable=True)
    published_at = Column(String, nullable=True)
    ai_title_used = Column(Boolean, default=False)
    ai_summary_used = Column(Boolean, default=False)
    ai_tags_used = Column(Boolean, default=False)
    ai_keywords_used = Column(Boolean, default=False)
    view_count = Column(BigInteger, default=0)
    download_count = Column(BigInteger, default=0)
    share_count = Column(BigInteger, default=0)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    search_vector = Column(TSVECTOR, nullable=True)
    deleted_at = Column(String, nullable=True)


class DocumentVersion(BaseModel):
    __tablename__ = "document_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    version = Column(String(20), nullable=False)
    storage_key = Column(String, nullable=True)
    file_size_bytes = Column(BigInteger, nullable=True)
    checksum_sha256 = Column(String(64), nullable=True)
    change_summary = Column(String, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)


class DocumentTag(BaseModel):
    __tablename__ = "document_tags"
    __table_args__ = {"extend_existing": True}

    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True)
    added_by_ai = Column(Boolean, default=False)
