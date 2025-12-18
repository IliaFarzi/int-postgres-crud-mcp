from typing import Optional, Literal

from pydantic import BaseModel


class QueryTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal['pending', 'in_progress', 'done']] = None
