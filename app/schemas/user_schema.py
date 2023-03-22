from pydantic import BaseModel

from typing import Optional


class BaseUser(BaseModel):
    email: str
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None

class UserCreate(BaseUser):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    

class User(BaseUser):
    id: int
    is_active: bool

    class Config:
        orm_mode = True