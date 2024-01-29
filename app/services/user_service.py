import uuid
from fastapi import BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Optional, Union

from app.api.dependencies.db_deps import get_db
from app.core.security import create_access_token, create_refresh_token
from app.repository import user_repo as repo, profile_repo
from app.utils.validation import email_vaildation


def create_profile(user, db):
    new_profile = profile_repo.profile_schemas.ProfileCreate(
        firstname=user.firstname,
        lastname=user.lastname,
    )
    profile: profile_repo.Profile = profile_repo.ProfileRepository(
        db_session=db
    ).create(obj=new_profile)

    return profile


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = repo.UserRepository(db_session=self.db)

    def authenticate(
        self, email: str, password: str
    ) -> Optional[repo.token_schema.TokenSchema]:
        user = self.repo.authenticate(
            email=email,
            password=password,
        )
        tokens = repo.token_schema.TokenSchema(
            access_token=create_access_token(sub=user.id),
            refresh_token=create_refresh_token(sub=user.id),
            token_type="bearer",
        )

        return tokens

    def get_all_users(
        self,
        limit: int = 100,
        skip: int = 0,
    ) -> list[repo.user_schemas.User]:
        return self.repo.list(limit=limit, skip=skip)

    def get_user_by_id(self, user_id: Union[str, uuid.uuid4]) -> repo.user_schemas.User:
        user = self.repo.get(id=user_id)

        return user

    def get_user_by_username(self, username: str) -> repo.user_schemas.User:
        user = self.repo.get(username=username)

        return user

    def get_user_by_email(self, email: str) -> repo.user_schemas.User:
        user = self.repo.get(email=email)

        return user

    def user_exists(self, user: repo.user_schemas.UserCreate) -> bool:
        return self.repo.email_already_exists(
            email=user.email
        ) or self.repo.username_already_exists(username=user.username)

    async def create_user(
        self,
        user: repo.user_schemas.UserCreate,
        background_tasks: BackgroundTasks,
        role: str | None,
    ) -> repo.token_schema.TokenSchema:
        if self.user_exists(user=user):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email or username already exists",
            )

        new_user = self.repo.create(user=user) # can pass profile here

        access_token = create_access_token(sub=new_user.id)

        tokens = repo.token_schema.TokenSchema(
            access_token=access_token,
            refresh_token=create_refresh_token(sub=new_user.id),
            token_type="bearer",
        )

        # email validation
        # email_vaildation(
        #     background_tasks=background_tasks,
        #     access_token=access_token,
        #     new_user=new_user,
        # )

        return tokens

    async def create_superuser(
        self,
        user: repo.user_schemas.UserCreate,
    ) -> repo.token_schema.TokenSchema:
        if self.user_exists(user=user):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email or username already exists",
            )

        new_user = self.repo.create_superuser(user=user)
        pass

    def update_user(
        self,
        user_id: Union[str, uuid.uuid4],
        user_update: repo.user_schemas.UserUpdate,
    ) -> repo.user_schemas.User:
        updated_user = self.repo.update(id=user_id, obj=user_update)

        return updated_user

    def delete_user(
        self,
        user: repo.user_schemas.User,
        user_id: Union[str, uuid.uuid4],
    ) -> int:
        if user_id == user.id or user.role == "admin":
            self.repo.delete(id=user_id)

            return user_id

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def verify_user(self, user: repo.user_schemas.User) -> repo.user_schemas.User:
        verified_user = self.repo.verify_user(user=user)

        return verified_user


def user_service_dep(db: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(db=db)
