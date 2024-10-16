from datetime import datetime
from document.app.models import History
from document.app.schemas import HistoryResponseSchema
from document.service.base import BaseGetService, BaseAddService, BaseUpdateService


class HistoryService(BaseGetService, BaseAddService, BaseUpdateService):
    model = History

    @classmethod
    async def get_history_by_datetime(cls, pacient_id: int, history_datetime: datetime) -> HistoryResponseSchema:
        return await cls.find_one_or_none(pacientId=pacient_id, date=history_datetime)
    