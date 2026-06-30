from uuid import UUID 
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.repositories.abstract.tag import TagRepository
from app.schemas.tag import TagUpdate


class SQLTagRepository(TagRepository):

    def __init__(self, db: Session):
        self.db = db
    def get(self, id: UUID) -> Optional[Tag]:
        return (
            self.db.query(Tag)
            .filter(Tag.id == id)
            .first()
        )
    

    def get_all(
            self,
            skip: int = 0,
            limit: int = 100
    ) -> List[Tag]:
        return (
            self.db.query(Tag)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create(self, obj):
        raise NotImplementedError(
            "Use create_tag instead"
        )
    
    def get_by_slug(
            self,
            slug: str
    ) -> Optional[Tag]:
        return (
            self.db.query(Tag)
            .filter(Tag.slug ==slug)
            .first()
        )
   
    def create_tag(
            self,
            name: str,
            slug: str) -> Tag:
        
        tag = Tag(
            name=name,
            slug=slug
        )
        
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)

        return tag
    

    def update(
            self,
            id: UUID,
            obj_in: TagUpdate

    ) -> Optional[Tag]:
        tag = self.get(id)

        if not tag:
            return None
        update_data = obj_in.model_dump(
            exclude_unset= True
        )

        for field, value in update_data.items():
            setattr(tag, field, value)

        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)

        return tag
    

    def delete(
            self,
            id: UUID
    ) -> bool:
        
        tag = self.get(id)


        if not tag:
            return False
        
        self.db.delete(tag)
        self.db.commit()

        return True
    
        
    

    