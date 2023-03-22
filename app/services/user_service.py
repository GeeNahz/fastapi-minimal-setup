from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.models.user_model import User
from app.schemas import user_schema
from app.core.security import generate_password_hash, verify_password

class UserService:
    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[user_schema.User]:
        user = UserService.get_user_by_email(db=db, email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None
        
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        return user

    @staticmethod
    def get_user_by_id(db: Session, id: int) -> user_schema.User:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {id} not found"
            )
        return user

    @staticmethod
    def get_all_users(db: Session) -> list[user_schema.User]:
        return db.query(User).all()

    @staticmethod
    def create_user(db: Session, user: user_schema.UserCreate) -> user_schema.User:
        password_hash = generate_password_hash(user.password)
        new_user = User(
            email=user.email,
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            hashed_password=password_hash
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def update_user(db: Session, user_id: int, updates: user_schema.UserUpdate) -> user_schema.User:
        user_data = UserService.get_user_by_id(db=db, id=user_id)

        user_data.email = updates.email or user_data.email
        user_data.firstname = updates.firstname or user_data.firstname
        user_data.lastname = updates.lastname or user_data.lastname
        user_data.username = updates.username or user_data.username

        db.commit()
        db.refresh(user_data)

        return user_data

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserService.get_user_by_id(db=db, id=user_id)

        db.delete(user)