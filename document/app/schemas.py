from datetime import datetime
from pydantic import BaseModel


class UserHistoryResponseSchema(BaseModel):
    date: datetime
    hospitalId: int
    doctorId: int
    room: str
    data: str


class HistoryResponseSchema(UserHistoryResponseSchema):
    pacientId: int