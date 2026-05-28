from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.sql.user import SQLUserRepository
from app.repositories.abstract.user import UserRepository


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return SQLUserRepository(db)
