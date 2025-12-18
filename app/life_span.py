from contextlib import asynccontextmanager

from fastapi import FastAPI
from langchain_mcp_adapters.client import MultiServerMCPClient

from service.agent_service import AgentService
from service.config_service import ConfigService
from service.task_service import TaskService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    config = ConfigService(override=True).config
    task_service = TaskService(url=str(config.db_url))

    mcp_client = MultiServerMCPClient(
        {"TaskManager": {"transport": "stdio", "command": "python", "args": ["./task_mcp_server.py"]}})
    tools = await mcp_client.get_tools()
    for t in tools:
        print(f"- {t.name}: {t.description}")
        print(t.args)
    agent_service = AgentService(tools=tools)

    app.state.config = config
    app.state.task_service = task_service
    app.state.agent_service = agent_service

    yield

    del mcp_client
    del tools
    del agent_service
    del task_service
    del config
