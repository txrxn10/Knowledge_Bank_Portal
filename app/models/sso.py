from sqlalchemy import Column, String, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.db.base import BaseModel
import uuid


class SSOConfig(BaseModel):
    __tablename__   = "sso_config"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider        = Column(String(16), nullable=False)
    display_name    = Column(String(100), nullable=False)
    allowed_domains = Column(ARRAY(String), nullable=True)
    enforce_domain  = Column(Boolean, default=False)
    client_id       = Column(String, nullable=False)
    client_secret   = Column(String, nullable=False)
    issuer_url      = Column(String, nullable=True)
    auth_endpoint   = Column(String, nullable=True)
    token_endpoint  = Column(String, nullable=True)
    default_role    = Column(String(11), nullable=True)
    require_mfa     = Column(Boolean, default=False)
    is_active       = Column(Boolean, default=True)


class SSOCredentials(BaseModel):
    __tablename__   = "sso_credentials"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id         = Column(UUID(as_uuid=True), nullable=False)
    provider        = Column(String(50), nullable=False)
    provider_uid    = Column(String(255), nullable=False)
    access_token    = Column(String, nullable=True)
    refresh_token   = Column(String, nullable=True)
    token_expires   = Column(String, nullable=True)
    raw_profile     = Column(JSON, nullable=True)
