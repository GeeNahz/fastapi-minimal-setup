from fastapi import FastAPI

from app.api.api_v1.router import api_v1_router
from app.core import config, db_config

app = FastAPI(
    title=config.settings.PROJECT_NAME,
    openapi_url=f"{config.settings.API_V1_STR}/openapi.json"
)

db_config.Base.metadata.create_all(bind=db_config.engine)

app.include_router(router=api_v1_router, prefix=config.settings.API_V1_STR)