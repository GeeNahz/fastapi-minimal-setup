from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from typing import Annotated
from pydantic import ValidationError

from app.api.dependencies import db_deps
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from app.schemas.token_schema import TokenSchema, TokenPayload
from app.services.user_service import UserService

auth_router = APIRouter()

@auth_router.post('/', summary="Create access and refresh token", response_model=TokenSchema)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(db_deps.get_db)]):
    user = UserService.authenticate(db=db, email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token" : create_access_token(sub=user.id),
        "refresh_token" : create_refresh_token(sub=user.id),
        "token_type" : "bearer"
    }


@auth_router.post("/refresh/", summary="Refresh access token", response_model=TokenSchema)
async def refresh_token(refresh_token: Annotated[str, Body(...)], db: Annotated[Session, Depends(db_deps.get_db)]):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        refresh_token_data = TokenPayload(**payload)
    except(JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={ "WWW-Authenticate" : "Bearer" }
        )
    
    user = UserService.get_user_by_id(db=db, id=refresh_token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid user token"
        )
    
    return {
        "access_token" : create_access_token(sub=user.id),
        "refresh_token" : create_refresh_token(sub=user.id),
        "token_type" : "bearer"
    }