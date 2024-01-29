from pydantic import BaseModel
from typing import Optional


class BaseUser(BaseModel):
    email: str
    username: Optional[str] = None
    firstname: Optional[str] = None
    middlename: Optional[str] = None
    lastname: Optional[str] = None


class UserCreate(BaseUser):
    password: str


class UserCreateSuperuser(UserCreate):
    is_staff: bool
    is_superuser: bool
    is_active: bool


class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    middlename: Optional[str] = None
    lastname: Optional[str] = None


class User(BaseUser):
    id: int
    is_active: bool

    class ConfigDict:
        from_attributes = True
