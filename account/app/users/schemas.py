from enum import Enum
from pydantic import BaseModel, Field


class UserRoles(str, Enum):
    ADMIN = 'Admin'
    MANAGER = 'Manager'
    DOCTOR = 'Doctor'
    USER = 'User'


class ShowUserSchema(BaseModel):
    id: int
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    username: str
    roles: list[UserRoles]