from fastapi import APIRouter


from app.api.api_v1.handlers import user
from app.api.auth import jwt, password

api_v1_router = APIRouter()

api_v1_router.include_router(user.user_router, prefix='/user', tags=['users'])
api_v1_router.include_router(jwt.auth_router, prefix='/token', tags=['tokens'])
api_v1_router.include_router(password.password_router, tags=['password'])
