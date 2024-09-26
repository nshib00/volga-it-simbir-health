from hospital.app.hospitals.models import Hospital
from hospital.app.service.base import BaseAddService, BaseDeleteService, BaseGetService, BaseUpdateService


class HospitalService(BaseGetService, BaseAddService, BaseUpdateService, BaseDeleteService):
    model = Hospital

    @classmethod
    async def get_hospital_rooms(cls, hospital_id: int) -> list[str] | None:
        hospital = await cls.find_one_or_none(id=hospital_id)
        if hospital is not None:
            return hospital.rooms
