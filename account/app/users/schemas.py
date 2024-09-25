from pydantic import BaseModel, Field


class ShowUserSchema(BaseModel):
    id: int
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    username: str
    roles: list[str]