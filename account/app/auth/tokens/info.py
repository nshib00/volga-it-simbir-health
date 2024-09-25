from dataclasses import dataclass
from pydantic import BaseModel


ACCESS_TOKEN_TYPE = 'access_token'
REFRESH_TOKEN_TYPE = 'refresh_token'


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str