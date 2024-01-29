from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from jose import jwt, JWTError
from pydantic import ValidationError

from app.core.config import settings
from app.core.security import create_access_token, generate_password_hash, verify_password
from app.schemas.email_schemas import EmailBody, EmailData, EmailPayload
from app.schemas.password_schemas import PasswordChange
from app.schemas.token_schema import TokenPayload
from app.schemas.user_schemas import User, UserUpdate
from app.services.user_service import UserService, user_service_dep
from app.utils.verify_user_util import Email


password_router = APIRouter()


@password_router.post(
    "/", summary="Send email for password reset", status_code=status.HTTP_202_ACCEPTED
)
async def send_email(
    service: Annotated[UserService, Depends(user_service_dep)],
    email: EmailPayload,
):
    user: User = await UserService.get_user_by_email(email=email)
    user = service.get_user_by_email(email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email does not exist"
        )
    access_token = create_access_token(subject=user.user_id, expires_delta=10)

    email_body = EmailBody(
        token=access_token,
        username=user.username,
    )
    email_data = EmailData(
        email=[email],
        body=email_body,
    )
    await Email().send_reset_password_mail(email=email_data)

    return {"message": "success"}


@password_router.post(
    "/reset",
    summary="Reset user's password",
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def reset_password(
    service: Annotated[
        UserService,
        Depends(user_service_dep),
    ],
    data: PasswordChange,
):
    data = data.model_dump()
    password = data.new_password
    token = data.token

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_password = generate_password_hash(password=password)
    user_password_update = UserUpdate(
        hashed_password=new_password,
    )
    user_update = service.update_user(
        user_id=token_data.sub, user_update=user_password_update
    )

    return user_update
