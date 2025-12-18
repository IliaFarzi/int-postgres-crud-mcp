from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel


class QueryTask(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal['pending', 'in_progress', 'done']] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
