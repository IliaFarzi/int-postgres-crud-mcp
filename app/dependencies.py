from fastapi import Request

from domain.model.config import Config
from service.agent_service import AgentService
from service.task_service import TaskService


def get_agent_service(request: Request) -> AgentService:
    return request.app.state.agent_service


def get_task_service(request: Request) -> TaskService:
    return request.app.state.task_service


def get_config(request: Request) -> Config:
    return request.app.state.config
