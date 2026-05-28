from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, func
from datetime import datetime

Base = declarative_base()


class BaseModel(Base):
    """Base model with common fields"""
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
