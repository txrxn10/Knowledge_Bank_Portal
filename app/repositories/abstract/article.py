from abc import abstractmethod
from uuid import UUID

from app.models.article import KnowledgeArticle
from app.repositories.abstract.base import BaseRepository


class ArticleRepository(BaseRepository[KnowledgeArticle]):

    @abstractmethod
    def get_by_slug(
        self,
        slug: str,
    ) -> KnowledgeArticle | None:
        pass

    @abstractmethod
    def create_article(
        self,
        article: KnowledgeArticle,
    ) -> KnowledgeArticle:
        pass

    @abstractmethod
    def list_articles(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[KnowledgeArticle]:
        pass

    @abstractmethod
    def get_article(
        self,
        article_id: UUID,
    ) -> KnowledgeArticle | None:
        pass


    @abstractmethod
    def get_latest_version(
        self,
        root_article_id: UUID,

    ) -> KnowledgeArticle | None:
        pass


    @abstractmethod
    def list_versions(
        self,
        root_article_id: UUID,
    ) -> list[KnowledgeArticle]:
        pass