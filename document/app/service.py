from datetime import datetime

from sqlalchemy import select
from document.app.models import History
from document.app.schemas import HistoryResponseSchema
from document.service.base import BaseGetService, BaseAddService, BaseUpdateService


class HistoryService(BaseGetService, BaseAddService, BaseUpdateService):
    model = History

    @classmethod
    async def get_history_by_datetime(cls, pacient_id: int, history_datetime: datetime) -> HistoryResponseSchema:
        return await cls.find_one_or_none(pacientId=pacient_id, date=history_datetime)
   

    @classmethod
    async def get_history_data_to_sync(cls):
        query = select(cls.model.date, cls.model.pacientId, cls.model.hospitalId, cls.model.doctorId, cls.model.data)
        result = await cls._get_result(query)
        result_mappings = result.mappings().all()
        return [
            {
                'date': mapping['date'],
                'pacientId': mapping['pacientId'],
                'hospitalId': mapping['hospitalId'],
                'doctorId': mapping['doctorId'],
                'data': mapping['data']
            } for mapping in result_mappings
        ]