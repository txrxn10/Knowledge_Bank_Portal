from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
from app.config import settings
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt



def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        print("PAYLOAD:", payload)

        user_id = payload.get("sub")

        print("USER_ID:", user_id)

        if not user_id:
            return None

        return UUID(user_id)

    except Exception as e:
        print("JWT ERROR:", e)
        return None
