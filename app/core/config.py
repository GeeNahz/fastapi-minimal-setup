from pydantic import AnyHttpUrl, ConfigDict
from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRATION: int = 15
    REFRESH_TOKEN_EXPIRATION: int = 60 + 24 + 7
    BACKEND_CORE_ORIGIN: list[AnyHttpUrl] = []
    PROJECT_NAME: str = "my_project_name"

    DATABASE_CONNECTION_STR: str = config("DATABASE_CONNECTION_STRING", cast=str)

    # email details
    MAIL_USERNAME: str = config("MAIL_USERNAME", cast=str)
    MAIL_PASSWORD: str = config("MAIL_PASSWORD", cast=str)
    MAIL_FROM: str = config("MAIL_FROM", cast=str)
    MAIL_PORT: str = config("MAIL_PORT", cast=str)
    MAIL_SERVER: str = config("MAIL_SERVER", cast=str)
    MAIL_FROM_NAME: str = config("MAIL_FROM_NAME", cast=str)


settings = Settings()
