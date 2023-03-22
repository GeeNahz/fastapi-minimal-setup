from sqlalchemy import Column, Boolean, Integer, String
# from sqlalchemy.orm import relationship # for database relationships

from app.core.db_config import Base

class User(Base):
    __tablename__ = "users" # plural form of the class name

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=True)
    firstname = Column(String(50), index=True, nullable=True)
    lastname = Column(String(50), index=True, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)