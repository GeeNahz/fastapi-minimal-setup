from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.api.dependencies import db_deps
from app.schemas.user_schema import UserCreate, UserUpdate, User
from app.services.user_service import UserService

user_router = APIRouter()


@user_router.post("/create/", summary="Create a user", response_model=User)
async def create(user: UserCreate, db: Annotated[Session, Depends(db_deps.get_db)]):
    email_exists = UserService.get_user_by_email(db=db, email=user.email)
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    new_user = UserService.create_user(db=db, user=user)
    return new_user

@user_router.put("/update/{user_id}", summary="Update a user", response_model=User)
async def update(user_id: int, user: UserUpdate, db: Annotated[Session, Depends(db_deps.get_db)]):
    updated_user = UserService.update_user(db=db, user_id=user_id, updates=user)
    return updated_user

@user_router.delete("/delete/", summary="Delete a user")
async def delete(user_id: int, db: Annotated[Session, Depends(db_deps.get_db)]):
    UserService.delete_user(db=db, user_id=user_id)
    return { "message": status.HTTP_204_NO_CONTENT, "detail": "User deleted" }

@user_router.get("/all/", summary="Get all user", response_model=list[User])
async def all_users(db: Annotated[Session, Depends(db_deps.get_db)]):
    return UserService.get_all_users(db=db)

@user_router.get("/{user_id}/", summary="Get user by their id", response_model=User)
async def one_user(user_id: int, db: Annotated[Session, Depends(db_deps.get_db)]):
    user = UserService.get_user_by_id(db=db, id=user_id)
    return user