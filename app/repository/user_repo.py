from typing import Any, Optional
import uuid
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.core.security import generate_password_hash, verify_password

from app.models.user_model import User
from app.models.profile_model import Profile
from app.repository.base_repo import BaseRepository
from app.schemas import user_schemas, profile_schemas, token_schema


class UserRepository(
    BaseRepository[User, user_schemas.UserCreate, user_schemas.UserUpdate]
):
    def __init__(self, db_session: Session):
        super(UserRepository, self).__init__(User, db_session)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        error = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

        user = self.get(email=email)

        if not user:
            raise error

        if not verify_password(password=password, hashed_password=user.hashed_password):
            raise error

        return user

    def create(
        self,
        user: user_schemas.UserCreate | user_schemas.UserCreateSuperuser,
        profile: Profile | None,
    ) -> User:
        hashed_password = generate_password_hash(password=user.password)

        new_user = User(
            **user.model_dump(exclude_unset=True),
            hashed_password=hashed_password,
            # profile=profile,
        )

        self.db_session.add(new_user)
        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print("Create error: ", e)
            self.db_session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Conflict Error"
                )
            else:
                raise e

        self.db_session.refresh(new_user)

        return new_user

    def create_superuser(
        self,
        user: user_schemas.UserCreate,
        profile: Profile | None,
    ) -> User:
        superuser = user_schemas.UserCreateSuperuser(
            user.model_dump(exclude_unset=True),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        new_user = self.create(superuser)

        return new_user

    def get(
        self,
        email: str | None = None,
        username: str | None = None,
        id: str | uuid.uuid4 | None = None,
    ) -> Optional[User]:
        if email is not None:
            stmt = sqlalchemy.select(self.model).where(self.model.email == email)
            user = self.db_session.execute(stmt).scalar()

            return user
        elif username is not None:
            stmt = sqlalchemy.select(self.model).where(self.model.username == username)
            user = self.db_session.execute(stmt).scalar()

            return user
        elif id is not None:
            return super().get(id=id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No search key was provided",
            )

    def email_already_exists(self, email: str) -> bool:
        stmt = sqlalchemy.select(self.model).where(self.model.email == email)
        email_exists = self.db_session.execute(stmt).scalar()
        return True if email_exists else False

    def username_already_exists(self, username: str) -> bool:
        stmt = sqlalchemy.select(self.model).where(self.model.username == username)
        username_exists = self.db_session.execute(stmt).scalar()

        return True if username_exists else False

    def verify_user(self, user: user_schemas.User) -> User:
        user_update = user_schemas.UserUpdate(is_verified=True)
        user_verified = self.update(id=user.id, obj=user_update)

        return user_verified


# think of a way to abstract password generation & validation and save it in one function
