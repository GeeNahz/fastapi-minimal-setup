from pydantic import BaseSettings, AnyHttpUrl
from decouple import config # takes values from env file. create one in app directory with the corresponding names


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRATION: int = 15
    REFRESH_TOKEN_EXPIRATION: int = 60 + 24 + 7
    BACKEND_CORE_ORIGIN: list[AnyHttpUrl] = []
    PROJECT_NAME: str = "myProject"

    DATABASE_CONNECTION_STR: str = config("DATABASE_CONNECTION_STR", cast=str)

settings = Settings()