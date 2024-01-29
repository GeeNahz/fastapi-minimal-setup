from datetime import datetime
import uuid
from pydantic import UUID4

from sqlalchemy import (
    Boolean,
    DateTime,
    String,
    Uuid,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.db_config import Base

now = datetime.utcnow


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID4] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True), primary_key=True, default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(
        String(200), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255))
    firstname: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    middlename: Mapped[str] = mapped_column(String(50), nullable=True)
    lastname: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    is_active: Mapped[str] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    modified_at: Mapped[datetime] = mapped_column(DateTime, default=now, onupdate=now)

    def __repr__(self) -> str:
        return f"User(email={self.email})"
