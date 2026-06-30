from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.sql.collection import SQLCollectionRepository
from app.services.collection import CollectionService
from app.schemas.collection import (
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
)

router = APIRouter(
    prefix="/collections",
    tags=["Master - Collections"]
)


@router.post(
    "",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_collection(
    collection_in: CollectionCreate,
    db: Session = Depends(get_db),
):
    service = CollectionService(
        SQLCollectionRepository(db)
    )

    try:
        return service.create_collection(
            collection_in
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "",
    response_model=List[CollectionResponse]
)
def list_collections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    service = CollectionService(
        SQLCollectionRepository(db)
    )

    return service.list_collections(
        skip,
        limit
    )


@router.get(
    "/{collection_id}",
    response_model=CollectionResponse
)
def get_collection(
    collection_id: UUID,
    db: Session = Depends(get_db),
):
    service = CollectionService(
        SQLCollectionRepository(db)
    )

    collection = service.get_collection(
        collection_id
    )

    if not collection:
        raise HTTPException(
            status_code=404,
            detail="Collection not found"
        )

    return collection


@router.put(
    "/{collection_id}",
    response_model=CollectionResponse
)
def update_collection(
    collection_id: UUID,
    collection_in: CollectionUpdate,
    db: Session = Depends(get_db),
):
    service = CollectionService(
        SQLCollectionRepository(db)
    )

    collection = service.update_collection(
        collection_id,
        collection_in
    )

    if not collection:
        raise HTTPException(
            status_code=404,
            detail="Collection not found"
        )

    return collection


@router.delete(
    "/{collection_id}"
)
def delete_collection(
    collection_id: UUID,
    db: Session = Depends(get_db),
):
    service = CollectionService(
        SQLCollectionRepository(db)
    )

    deleted = service.delete_collection(
        collection_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Collection not found"
        )

    return {
        "message": "Collection deleted successfully"
    }