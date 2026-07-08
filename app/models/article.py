from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    BigInteger,
    ForeignKey,
    ARRAY,
    Enum,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR

from app.db.base import BaseModel
import uuid

from app.enums.document_status import DocumentStatus
from app.enums.resource_visibility import ResourceVisibility
from app.enums.approval_status import ApprovalStatus


class KnowledgeArticle(BaseModel):
    __tablename__ = "knowledge_articles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(
        String(400),
        nullable=False
    )

    slug = Column(
        String(400),
        nullable=False,
        unique=True
    )

    description = Column(
        Text,
        nullable=True
    )

    summary = Column(
        Text,
        nullable=True
    )

    status = Column(
    Enum(
        DocumentStatus,
        values_callable=lambda x: [e.value for e in x],
        name="document_status",
    ),
    nullable=False,
    default=DocumentStatus.DRAFT,
)

    visibility = Column(
    Enum(
        ResourceVisibility,
        values_callable=lambda x: [e.value for e in x],
        name="resource_visibility",
    ),
    nullable=False,
    default=ResourceVisibility.INTERNAL,
)

    keywords = Column(
        ARRAY(String),
        nullable=True
    )

    tags = Column(
        ARRAY(String),
        nullable=True
    )

    is_featured = Column(
        Boolean,
        default=False,
        nullable=False
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    version = Column(
        String(20),
        default="1.0",
        nullable=False
    )

    version_notes = Column(
        Text,
        nullable=True
    )

    parent_article_id = Column(
        UUID(as_uuid=True),
        ForeignKey("knowledge_articles.id"),
        nullable=True
    )

    is_latest_version = Column(
        Boolean,
        default=True,
        nullable=False
    )

    approval_status = Column(
    Enum(
        ApprovalStatus,
        values_callable=lambda x: [e.value for e in x],
        name="approval_status",
    ),
    nullable=False,
    default=ApprovalStatus.DRAFT,
)

    approved_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    approved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    published_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    submitted_for_review_at = Column(
    DateTime(timezone=True),
    nullable=True
    )

    submitted_for_review_by = Column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=True
    )

    review_comments = Column(
    Text,
    nullable=True
    )

    view_count = Column(
        BigInteger,
        default=0,
        nullable=False
    )

    download_count = Column(
        BigInteger,
        default=0,
        nullable=False
    )

    share_count = Column(
        BigInteger,
        default=0,
        nullable=False
    )

    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    updated_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    search_vector = Column(
    TSVECTOR,
    nullable=True
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )