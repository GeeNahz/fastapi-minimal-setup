import enum
from datetime import datetime
import uuid
from pydantic import UUID4
from sqlalchemy import (
    ForeignKey,
    String,
    Enum,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from typing import Optional

from app.core.db_config import Base


class GenderEnum(enum.Enum):
    male = "m", "male"
    female = "f", "female"
    others = "o", "others"
    none = "n", "none"


now = datetime.utcnow


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[UUID4] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True), primary_key=True, default=uuid.uuid4
    )
    firstname: Mapped[str] = mapped_column(String(length=50), index=True)
    lastname: Mapped[str] = mapped_column(String(length=50), index=True)
    # gender: Mapped[GenderEnum] = mapped_column(default=GenderEnum.none)
    # date_of_birth: Mapped[datetime | None] = mapped_column(default=now)

    # relationships
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")

    created_at: Mapped[datetime] = mapped_column(default=now)
    modified_at: Mapped[datetime] = mapped_column(default=now, onupdate=now)

    def __repr__(self) -> str:
        return f"Profile(id={self.id}, firstname={self.firstname}, lastname={self.lastname})"
