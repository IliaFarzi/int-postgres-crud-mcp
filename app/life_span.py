from contextlib import asynccontextmanager

from fastapi import FastAPI

from service.config_service import ConfigService
from service.task_service import TaskService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    config = ConfigService(override=True).config
    task_service = TaskService(url=str(config.db_url))

    app.state.config = config
    app.state.task_service = task_service

    yield

    del task_service
    del config
