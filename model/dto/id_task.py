from typing import Optional

from pydantic import BaseModel


class IdTask(BaseModel):
    id: Optional[int] = None
