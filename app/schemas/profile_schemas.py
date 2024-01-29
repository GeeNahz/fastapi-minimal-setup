from datetime import datetime

from pydantic import BaseModel
# from models.profile_model import Profile


class BaseProfile(BaseModel):
    firstname: str | None = None
    lastname: str | None = None

class ProfileCreate(BaseProfile):
    pass

class ProfileUpdate(BaseProfile):

    pass

class Profile(BaseProfile):
    id: int
    user_id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True