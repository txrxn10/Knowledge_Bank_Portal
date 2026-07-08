from enum import Enum


class DocumentStatus(str, Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"