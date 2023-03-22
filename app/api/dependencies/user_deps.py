from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from typing import Annotated
from jose import jwt, JWTError
from pydantic import ValidationError

from app.api.dependencies import db_deps
from app.core.config import settings
from app.schemas import token_schema, user_schema
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/token/",
    scheme_name="JWT"
)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(db_deps.get_db)]) -> user_schema.User:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = token_schema.TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Expired token",
                headers={ "WWW-Authenticate" : "Bearer" }
            )
    except(JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={ "WWW-Authenticate" : "Bearer" }
        )
    
    user = UserService.get_user_by_id(db=db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def get_current_active_user(user: Annotated[ user_schema.User, Depends(get_current_user)]) -> user_schema.User:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active"
        )
    return user

# def get_admin_user(user: Annotated[user_schema.User, Depends(get_current_active_user)]) -> user_schema.User:
    if not user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin"
        )
    return user