from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Literal['pending', 'in_progress', 'done']
    created_at: datetime
    updated_at: datetime
