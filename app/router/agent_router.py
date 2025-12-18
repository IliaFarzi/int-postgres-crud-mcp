from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies import get_agent_service
from service.agent_service import AgentService

agent_router = APIRouter(prefix="/agent")


@agent_router.post("ask", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_task(payload: str, agent_service: AgentService = Depends(get_agent_service)):
    try:
        return await agent_service.ask_agent(payload=payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
