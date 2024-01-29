from datetime import datetime, timedelta
from typing import Union, Any

from passlib.context import CryptContext
from jose import jwt

from app.core.config import settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def set_expires_delta(expires_delta: Union[int, None] = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRATION
        )
    return expires_delta


def generate_password_hash(password: str) -> str:
    return password_context.hash(secret=password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(secret=password, hash=hashed_password)


def create_access_token(
    sub: Union[str, Any],
    expires_delta: Union[int, None] = None,
) -> str:
    exp_delta = set_expires_delta(expires_delta=expires_delta)

    to_encode = {"exp": exp_delta, "sub": str(sub)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def create_refresh_token(
    sub: Union[str, Any],
    expires_delta: Union[int, None] = None,
) -> str:
    exp_delta = set_expires_delta(expires_delta=expires_delta)

    to_encode = {"exp": exp_delta, "sub": str(sub)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM
    )

    return encoded_jwt
