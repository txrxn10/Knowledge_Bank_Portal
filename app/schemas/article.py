from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.enums.document_status import DocumentStatus
from app.enums.resource_visibility import ResourceVisibility
from app.enums.approval_status import ApprovalStatus


class ArticleCreate(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    summary: Optional[str] = None
    visibility: ResourceVisibility = ResourceVisibility.INTERNAL
    keywords: list[str] = []
    tags: list[str] = []


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    visibility: Optional[ResourceVisibility] = None
    keywords: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    status: Optional[DocumentStatus] = None
    approval_status: Optional[ApprovalStatus] = None


class ArticleResponse(BaseModel):
    id: UUID
    title: str
    slug: str

    version: str
    parent_article_id: Optional[UUID]
    is_latest_version: bool

    description: Optional[str]
    summary: Optional[str]

    status: DocumentStatus
    visibility: ResourceVisibility

    keywords: list[str]
    tags: list[str]

    approval_status: ApprovalStatus

    submitted_for_review_at: Optional[datetime]
    review_comments: Optional[str]

    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    published_at: Optional[datetime]

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
