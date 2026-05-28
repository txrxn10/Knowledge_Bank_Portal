from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    
    # App
    APP_NAME: str = "Knowledge Bank API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@host.docker.internal:5432/kbms_v1?sslmode=disable"

    # Security
    SECRET_KEY: str = "kf7GbNL0J2RxFovHsii8TEVf19qxbUpGQCgfQvCKRGk="
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000", 
        "http://localhost:8000"
    ]

    # API
    API_V1: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
