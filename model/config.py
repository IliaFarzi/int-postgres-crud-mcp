from pydantic import BaseModel, Field, AnyUrl


class Config(BaseModel):
    openai_api_key: str = Field(..., min_length=1)
    db_url: AnyUrl
