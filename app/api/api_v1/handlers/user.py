import uuid
from sqlalchemy.orm import Session
from typing import Annotated, List

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    status,
)

from app.api.dependencies import db_deps, user_deps
from app.schemas.user_schemas import UserCreate, UserUpdate, User
from app.schemas.token_schema import TokenSchema
from app.services.user_service import UserService, user_service_dep

user_router = APIRouter()


@user_router.post(
    "/",
    summary="Create a user",
    response_model=TokenSchema,
)
async def create_user(
    user: UserCreate,
    service: Annotated[
        UserService,
        Depends(user_service_dep),
    ],
    background_tasks: BackgroundTasks,
    role: str = None,
):
    tokens = await service.create_user(
        user=user, background_tasks=background_tasks, role=role
    )

    return tokens


@user_router.put("/update-me", summary="update current user", response_model=User)
async def update_me(
    user: UserUpdate,
    current_user: Annotated[
        User,
        Depends(user_deps.get_current_active_user),
    ],
    service: Annotated[
        UserService,
        Depends(user_service_dep),
    ],
):
    updated_user_data = service.update_user(user_id=current_user.id, user_update=user)

    return updated_user_data


@user_router.put("/{user_id}", summary="Update a user", response_model=User)
async def update_user(
    user_id: str | uuid.uuid4,
    user: UserUpdate,
    service: Annotated[
        UserService,
        Depends(user_service_dep),
    ],
):
    updated_user = service.update_user(user_id=user_id, user_update=user)

    return updated_user


@user_router.delete("/", summary="Delete a user")
async def delete_user(
    user_id: str | uuid.uuid4,
    user: Annotated[
        User,
        Depends(user_deps.get_current_active_user),
    ],
    service: Annotated[
        UserService,
        Depends(user_service_dep),
    ],
):
    service.delete_user(user=user, user_id=user_id)

    return {
        "message": status.HTTP_204_NO_CONTENT,
        "detail": "User deleted",
    }


@user_router.get("/", summary="Get all user", response_model=List[User])
async def get_users(
    service: Annotated[
        UserService,
        Depends(user_service_dep),
    ],
    limit: int = None,
    skip: int = None,
):
    return service.get_all_users(limit=limit, skip=skip)


@user_router.get("/{user_id}/", summary="Get user by id", response_model=User)
async def get_user(
    user_id: str | uuid.uuid4,
    active_user: Annotated[
        User,
        Depends(user_deps.get_current_active_user),
    ],
    service: Annotated[
        UserService,
        Depends(user_service_dep)
    ],
    db: Annotated[Session, Depends(db_deps.get_db)],
):
    return service.get_user_by_id(user_id=user_id)
