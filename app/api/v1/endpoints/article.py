from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.models.user import User
from app.schemas.article import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
)

from app.services.article import ArticleService

from app.dependencies import (
    get_article_service,
    get_article_repository,
    get_current_user,
)

from app.repositories.abstract.article import (
    ArticleRepository,
)

from app.core.exceptions import (
    NotFoundException,
    ConflictException,
)

router = APIRouter(
    prefix="/articles",
    tags=["Knowledge Articles"],
)



@router.post(
    "",
    response_model=ArticleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_article(
    article_in: ArticleCreate,
    current_user=Depends(
        get_current_user
    ),
    article_service: ArticleService = Depends(
        get_article_service
    ),
):
    try:
        return article_service.create_article(
            article_in,
            current_user.id,
        )
    except ValueError as e:
        raise ConflictException(
            detail=str(e)
        )
    


@router.get(
    "/pending-review",
    response_model=list[ArticleResponse],
)
def list_pending_review_articles(
    article_service: ArticleService = Depends(
        get_article_service
    ),
):
    return article_service.list_pending_review_articles()
    



@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
)
def get_article(
    article_id: UUID,
    repo: ArticleRepository = Depends(
        get_article_repository
    ),
):
    article = repo.get_article(
        article_id
    )

    if not article:
        raise NotFoundException(
            detail="Article not found"
        )

    return article    



@router.get(
    "",
    response_model=list[ArticleResponse],
)
def list_articles(
    skip: int = 0,
    limit: int = 100,
    repo: ArticleRepository = Depends(
        get_article_repository
    ),
):
    return repo.list_articles(
        skip,
        limit,
    )



@router.put(
    "/{article_id}",
    response_model=ArticleResponse,
)
def update_article(
    article_id: UUID,
    article_in: ArticleUpdate,
    current_user=Depends(
        get_current_user
    ),
    article_service: ArticleService = Depends(
        get_article_service
    ),
):
    try:
        return article_service.update_article(
            article_id,
            article_in,
            current_user.id,
        )
    except ValueError:
        raise NotFoundException(
            detail="Article not found"
        )
    



@router.delete(
    "/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_article(
    article_id: UUID,
    article_service: ArticleService = Depends(
        get_article_service
    ),
):
    try:
        article_service.delete_article(
            article_id
        )
    except ValueError:
        raise NotFoundException(
            detail="Article not found"
        )

    return None



@router.post(
    "/{article_id}/submit-review",
    response_model=ArticleResponse,
)
def submit_article_for_review(
    article_id: UUID,
    current_user=Depends(
        get_current_user
    ),
    article_service: ArticleService = Depends(
        get_article_service
    ),
):
    try:
        return article_service.submit_for_review(
            article_id,
            current_user.id,
        )

    except ValueError as e:
        raise ConflictException(
            detail=str(e)
        )
    



@router.post(
    "/{article_id}/approve",
    response_model=ArticleResponse,
    summary="Approve Article",
)
def approve_article(
    article_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    article_service: ArticleService = Depends(
        get_article_service,
    ),
):
    try:
        return article_service.approve_article(
            article_id,
            current_user.id,
        )

    except ValueError as e:
        raise ConflictException(
            detail=str(e)
        )
    




@router.post(
    "/{article_id}/versions",
    response_model=ArticleResponse,
)
def create_article_version(
    article_id: UUID,
    current_user=Depends(
        get_current_user
    ),
    article_service: ArticleService = Depends(
        get_article_service
    ),
):
    try:
        return article_service.create_new_version(
            article_id,
            current_user.id,
        )
    except ValueError:
        raise NotFoundException(
            detail="Article not found"
        )
    




@router.get(
    "/{article_id}/versions",
    response_model=list[ArticleResponse],
)
def list_article_versions(
    article_id: UUID,
    article_service: ArticleService = Depends(
        get_article_service 
    ),
):
    try:
        return article_service.list_versions(
            article_id
        )
    except ValueError:
        raise NotFoundException(
            detail="Article not found"
        )
    



@router.get(
    "/{article_id}/latest",
    response_model=ArticleResponse,
)

def get_latest_article_version(
    article_id: UUID,
    article_service: ArticleService = Depends(
        get_article_service
    ),
):
    try:
        return article_service.get_latest_version(
            article_id
        )
    except ValueError:
        raise NotFoundException(
            detail="Article not found"
        )
    

    

    