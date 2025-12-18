from typing import Optional, Literal

from pydantic import BaseModel


class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None
    status: Literal['pending', 'in_progress', 'done'] = 'pending'
