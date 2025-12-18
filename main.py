from fastapi import FastAPI

from app.life_span import lifespan
from app.router.agent_router import agent_router
from app.router.task_router import task_router as task_router

app = FastAPI(title="TaskManagement", lifespan=lifespan)

app.include_router(task_router)
app.include_router(agent_router)
