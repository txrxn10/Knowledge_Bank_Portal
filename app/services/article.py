from datetime import datetime
from uuid import UUID

from app.enums.approval_status import ApprovalStatus
from app.enums.document_status import DocumentStatus
from app.models import article
from app.models.article import KnowledgeArticle
from app.repositories.sql.article import SQLArticleRepository
from app.schemas.article import (
    ArticleCreate,
    ArticleUpdate,
)


class ArticleService:
    def __init__(
        self,
        article_repository: SQLArticleRepository,
    ):
        self.article_repository = article_repository

    def create_article(
        self,
        article_data: ArticleCreate,
        created_by: UUID,
    ) -> KnowledgeArticle:

        existing = self.article_repository.get_by_slug(
            article_data.slug
        )

        if existing:
            raise ValueError(
                "Article with this slug already exists."
            )

        article = KnowledgeArticle(
            title=article_data.title,
            slug=article_data.slug,
            description=article_data.description,
            summary=article_data.summary,
            visibility=article_data.visibility,
            keywords=article_data.keywords,
            tags=article_data.tags,
            status=DocumentStatus.DRAFT,
            approval_status=ApprovalStatus.DRAFT,
            created_by=created_by,
            updated_by=created_by,
        )

        return self.article_repository.create_article(
            article
        )

    def list_articles(
        self,
        skip: int = 0,
        limit: int = 100,
    ):
        return self.article_repository.list_articles(
            skip,
            limit,
        )

    def get_article(
        self,
        article_id: UUID,
    ):
        article = self.article_repository.get_article(
            article_id
        )

        if not article:
            raise ValueError(
                "Article not found."
            )

        return article

    def update_article(
        self,
        article_id: UUID,
        article_data: ArticleUpdate,
        updated_by: UUID,
    ):
        article = self.get_article(
            article_id
        )

        update_data = article_data.model_dump(
            exclude_unset=True
        )

        try:
            for field, value in update_data.items():
                setattr(
                    article,
                    field,
                    value,
                )

            article.updated_by = updated_by

            self.article_repository.db.commit()
            self.article_repository.db.refresh(article)

            return article

        except Exception:
            self.article_repository.db.rollback()
            raise

    def delete_article(
        self,
        article_id: UUID,
    ):
        article = self.get_article(
            article_id
        )

        try:
            article.deleted_at = datetime.utcnow()

            self.article_repository.db.commit()

            return True

        except Exception:
            self.article_repository.db.rollback()
            raise


    def submit_for_review(
    self,
    article_id: UUID,
    submitted_by: UUID,
    ):
        article = self.get_article(article_id)

        if article.status != DocumentStatus.DRAFT:
            raise ValueError(
            "Only draft articles can be submitted for review."
        )

        article.status = DocumentStatus.UNDER_REVIEW
        article.approval_status = ApprovalStatus.PENDING_REVIEW
        article.submitted_for_review_at = datetime.utcnow()
        article.submitted_for_review_by = submitted_by
        article.updated_by = submitted_by

        try:
            self.article_repository.db.commit()
            self.article_repository.db.refresh(article)
            return article

        except Exception:
            self.article_repository.db.rollback()
            raise



    def approve_article(
        self,
        article_id: UUID,
        approved_by: UUID,
    ):
            article = self.get_article(article_id)

            if (
            article.status != DocumentStatus.UNDER_REVIEW
            or article.approval_status != ApprovalStatus.PENDING_REVIEW
            ):
                raise ValueError(
                "Article is not pending review."
                )

            try:
                article.status = DocumentStatus.PUBLISHED
                article.approval_status = ApprovalStatus.APPROVED

                article.approved_by = approved_by
                article.approved_at = datetime.now()

                article.published_at = datetime.now()

                article.updated_by = approved_by

                self.article_repository.db.commit()
                self.article_repository.db.refresh(article)

                return article

            except Exception:
                self.article_repository.db.rollback()
                raise

    



    def create_new_version(
        self,
        article_id: UUID,
        updated_by: UUID,
    ):
        current_article = self.get_article(
            article_id
        )

        try:
            current_article.is_latest_version = False

            major, minor = map(
                int,
                current_article.version.split(".")
            )

            new_version = f"{major}.{minor + 1}"

            root_article_id = (
                current_article.parent_article_id
                or current_article.id
            )

            article = KnowledgeArticle(
                title=current_article.title,
                slug=current_article.slug,
                description=current_article.description,
                summary=current_article.summary,
                visibility=current_article.visibility,
                keywords=current_article.keywords,
                tags=current_article.tags,
                status=current_article.status,
                approval_status=ApprovalStatus.DRAFT,
                version=new_version,
                parent_article_id=root_article_id,
                is_latest_version=True,
                created_by=updated_by,
                updated_by=updated_by,
            )

            self.article_repository.db.add(article)
            self.article_repository.db.commit()
            self.article_repository.db.refresh(article)

            return article

        except Exception:
            self.article_repository.db.rollback()
            raise


    def list_versions(
        self,
        article_id: UUID,
    ):
        return self.article_repository.list_versions(
            article_id
        )

    def get_latest_version(
        self,
        article_id: UUID,
    ):
        article = self.article_repository.get_latest_version(
            article_id
        )

        if not article:
            raise ValueError(
                "Article not found."
            )

        return article
    
    def list_pending_review_articles(
            self,
    ):
        return self.article_repository.list_pending_review_articles()