# from typing import Annotated
# from sqlalchemy.orm import Session

# from fastapi import Depends

# from app.api.dependencies.db_deps import get_db
# from app.models.profile_model import Profile
# from app.repository.base_repo import BaseRepository
# from app.schemas import profile_schemas


# class ProfileRepository(
#     BaseRepository[
#         Profile,
#         profile_schemas.ProfileCreate,
#         profile_schemas.ProfileUpdate,
#     ]
# ):
#     def __init__(self, db_session: Session):
#         super(ProfileRepository, self).__init__(Profile, db_session)


# def profile_repo(db: Annotated[Session, Depends(get_db)]) -> ProfileRepository:
#     return ProfileRepository(db_session=db)
