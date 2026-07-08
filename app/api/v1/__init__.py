from fastapi import APIRouter
from app.api.v1.endpoints import collection

from app.api.v1.endpoints import (
    auth,
    users,
    department,
    category,
    tag,
    article,
    health
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(department.router)
api_router.include_router(category.router)
api_router.include_router(tag.router)
api_router.include_router(collection.router)
api_router.include_router(article.router)
api_router.include_router(health.router)