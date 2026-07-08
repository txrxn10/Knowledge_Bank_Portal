from ast import stmt
from unittest import skip
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.approval_status import ApprovalStatus
from app.models.article import KnowledgeArticle
from app.repositories.abstract.article import ArticleRepository


class SQLArticleRepository(ArticleRepository):
    def __init__(self, db: Session):
        self.db = db
        

    def get_by_slug(
        self,
        slug: str,
    ) -> KnowledgeArticle | None:
        stmt = select(KnowledgeArticle).where(
            KnowledgeArticle.slug == slug,
            KnowledgeArticle.deleted_at.is_(None),
        )
        return self.db.scalar(stmt)

    def create_article(
        self,
        article: KnowledgeArticle,
    ) -> KnowledgeArticle:
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def list_articles(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[KnowledgeArticle]:
        stmt = (
            select(KnowledgeArticle)
            .where(
                KnowledgeArticle.deleted_at.is_(None),
                KnowledgeArticle.is_latest_version.is_(True),
            )
        
        .order_by(KnowledgeArticle.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
        return list(self.db.scalars(stmt).all())
    


    def list_pending_review_articles(
    self,
    ) -> list[KnowledgeArticle]:
            stmt = (
            select(KnowledgeArticle)
            .where(
                KnowledgeArticle.deleted_at.is_(None),
                KnowledgeArticle.approval_status == ApprovalStatus.PENDING_REVIEW,
            )
            .order_by(
                KnowledgeArticle.submitted_for_review_at.desc()
            )
        )

            return list(self.db.scalars(stmt).all())

    def get_article(
        self,
        article_id: UUID,
    ) -> KnowledgeArticle | None:
        stmt = select(KnowledgeArticle).where(
            KnowledgeArticle.id == article_id,
            KnowledgeArticle.deleted_at.is_(None),
        )
        return self.db.scalar(stmt)
    

    def get_latest_version(
        self,
        root_article_id: UUID,
    ) -> KnowledgeArticle | None:
        stmt = (
            select(KnowledgeArticle)
            .where(
                (KnowledgeArticle.id == root_article_id) | (KnowledgeArticle.parent_article_id == root_article_id),
                KnowledgeArticle.is_latest_version.is_(True),
                KnowledgeArticle.deleted_at.is_(None),
            )
            .limit(1)
        )
        return self.db.scalar(stmt)


    def get(
        self,
        id: UUID
    ) -> KnowledgeArticle | None:
        return self.get_article(id)
    

        

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[KnowledgeArticle]:
        return self.list_articles(
            skip,
            limit,
        )

    def create(
        self,
        obj,
    ):
        raise NotImplementedError(
            "Use create_article instead"
        )

    def update(
        self,
        id: UUID,
        obj_in,
    ):
        raise NotImplementedError(
            "Use ArticleService.update_article instead"
        )

    def delete(
        self,
        id: UUID,
    ):
        raise NotImplementedError(
            "Use ArticleService.delete_article instead"
        )
    


    def list_versions(
        self,
        root_article_id: UUID,
        ) -> list[KnowledgeArticle]:
        stmt = (
            select(KnowledgeArticle)
            .where(
            (KnowledgeArticle.id == root_article_id)
            | (
                KnowledgeArticle.parent_article_id == root_article_id
                ),
                KnowledgeArticle.deleted_at.is_(None),
            )
            .order_by(
                KnowledgeArticle.created_at.desc()
            )
        )

        return list(self.db.scalars(stmt).all())

