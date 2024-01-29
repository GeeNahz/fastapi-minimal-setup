import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from pydantic import BaseModel
from typing import Any, Generic, List, Optional, Type, TypeVar

from core.db_config import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db_session: Session):
        self.model = model
        self.db_session = db_session

    def get(self, id: Any) -> Optional[ModelType]:
        stmt = sqlalchemy.select(self.model).where(self.model.id == id)
        obj: Optional[ModelType] = self.db_session.execute(stmt).scalar()
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )
        return obj
    
    def list(self, limit: int = 100, skip: int = 0) -> List[ModelType]:
        # TODO: implement pagination using limit and skip parameters
        stmt = sqlalchemy.select(self.model).offset(offset=skip).limit(limit=limit).order_by(self.model.id.asc(), self.model.created_at)
        objs: List[ModelType] = self.db_session.execute(stmt).scalars().all()
        return objs
    
    def create(self, obj: CreateSchemaType) -> ModelType:
        db_obj: ModelType = self.model(**obj.dict())
        self.db_session.add(db_obj)
        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print("Create error: ", e)
            self.db_session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conflict Error"
                )
            else:
                raise e
        self.db_session.refresh(db_obj)
        return db_obj
    
    def update(self, id: Any, obj: UpdateSchemaType) -> Optional[ModelType]:
        db_obj = self.get(id=id)
        for column, value in obj.dict(exclude_unset=True).items():
            setattr(db_obj, column, value)
        self.db_session.commit()
        return db_obj
    
    def delete(self, id: Any) -> None:
        db_obj = self.get(id=id)
        self.db_session.delete(db_obj)
        self.db_session.commit()