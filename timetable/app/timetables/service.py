from datetime import datetime, timedelta
from sqlalchemy import and_, delete, select

from timetable.app.exceptions import (
    AppointmentsExistException,
    TimeAlreadyTakenException,
    TimetableNotFoundException,
)
from timetable.app.service.base import BaseAddService, BaseDeleteService, BaseGetService, BaseUpdateService
from timetable.app.timetables.models import Appointment, Timetable
from timetable.app.timetables.checkers import DateValidator


class BaseTimetableService(BaseGetService, BaseDeleteService, DateValidator):
    model = Timetable

    @classmethod
    def _get_timetables_query(cls, date_from: datetime, date_to: datetime, *filters):
        return select(cls.model).filter(
            and_(
                cls.model.from_ >= date_from,
                cls.model.to <= date_to
            ),
            *filters,
        ) 

    @classmethod
    async def find_all_timetables(cls, date_from: datetime, date_to: datetime, *filters):
        date_from, date_to = cls.get_validated_dates(date_from, date_to)
        query = cls._get_timetables_query(date_from, date_to, *filters)
        result = await cls._get_result(query)
        return result.scalars().all()


class MainTimetableService(BaseAddService, BaseGetService, BaseDeleteService, BaseUpdateService, DateValidator):
    model = Timetable

    @classmethod
    async def add_timetable(
        cls,
        hospitalId: int,
        doctorId: int,
        from_: datetime,
        to: datetime,
        room: str,
    ) -> None:
        date_from, date_to = cls.get_validated_dates(date_from=from_, date_to=to, check_time_delta=True)
        await cls.add(
            hospitalId=hospitalId,
            doctorId=doctorId,
            from_=date_from,
            to=date_to,
            room=room,
        )
    
    @classmethod
    async def update_timetable(
        cls, 
        timetableId: int,
        hospitalId: int,
        doctorId: int,
        from_: datetime,
        to: datetime,
        room: str,
    ) -> None:
        date_from, date_to = cls.get_validated_dates(date_from=from_, date_to=to, check_time_delta=True)
        taken_appointments = await AppointmentService.get_taken_appoinments(timetable_id=timetableId)
        if taken_appointments:
            raise AppointmentsExistException
        await cls.update_one(
            model_id=timetableId,
            hospitalId=hospitalId,
            doctorId=doctorId,
            from_=date_from,
            to=date_to,
            room=room,
        )
 
    @classmethod
    async def _get_timetable_by_id(cls, timetable_id: int) -> Timetable:
        timetable = await cls.find_one_or_none(id=timetable_id)
        if timetable is None:
            raise TimetableNotFoundException
        return timetable


class TimetableDoctorService(BaseTimetableService):
    @classmethod
    async def find_doctor_timetables(cls, doctor_id: int, date_from: datetime, date_to: datetime):
        date_from, date_to = cls.get_validated_dates(date_from, date_to)
        await cls.find_all_timetables(
            date_from=date_from,
            date_to=date_to,
            doctor_id=doctor_id,
        )

    @classmethod
    async def delete_doctor_timetables(cls, doctor_id: int):
        doctor_timetables_query = select(cls.model.__table__.columns).where(cls.model.doctorId == doctor_id)
        doctor_timetables_result = await cls._get_result(doctor_timetables_query)
        doctor_timetable_ids = [
            timetable['id'] for timetable in doctor_timetables_result.mappings().all()
        ]
        for doctor_timetable_id in doctor_timetable_ids:
            await cls.delete_one(model_id=doctor_timetable_id)

        
class TimetableHospitalService(BaseTimetableService):
    @classmethod
    async def find_hospital_timetables(cls, hospital_id: int, date_from: datetime, date_to: datetime):
        date_from, date_to = cls.get_validated_dates(date_from, date_to)
        await cls.find_all_timetables(
            date_from=date_from,
            date_to=date_to,
            hospital_id=hospital_id,
        )

    @classmethod
    async def delete_hospital_timetables(cls, doctor_id: int):
        hospital_timetables_query = select(cls.model.__table__.columns).where(cls.model.doctorId == doctor_id)
        hospital_timetables_result = await cls._get_result(hospital_timetables_query)
        hospital_timetable_ids = [
            timetable['id'] for timetable in hospital_timetables_result.mappings().all()
        ]
        for hospital_timetable_id in hospital_timetable_ids:
            await cls.delete_one(model_id=hospital_timetable_id)

    @classmethod
    async def get_room_timetables(cls, room: str, from_: datetime, to: datetime):
        date_from, date_to = cls.get_validated_dates(from_, to)
        room_timetables_query = cls._get_timetables_query(
            date_from,
            date_to,
            cls.model.room == str(room)
        )
        room_timetables_result = await cls._get_result(room_timetables_query)
        return room_timetables_result.scalars().all()
    

class AppointmentService(BaseGetService, BaseAddService, BaseDeleteService):
    model = Appointment

    @classmethod
    def get_appointments(cls, date_from: datetime, date_to: datetime) -> list[str]:
        date_from, date_to = DateValidator.get_validated_dates(date_from, date_to)
        date_delta_minutes = (date_to - date_from).seconds // 60
        appointments = []
        for half_hour in range(0, date_delta_minutes-30+1, 30):
            appointments.append(date_from + timedelta(minutes=half_hour))
        return appointments
    
    @classmethod
    async def get_taken_appoinments(cls, timetable_id: int) -> list[str]:
        appointments_from_db = await cls.find_all(timetable_id=timetable_id)
        return [
            appointment.from_ for appointment in appointments_from_db
        ]
    
    @classmethod
    async def get_free_appointments(cls, timetable_id: int) -> list[str]:
        timetable = await MainTimetableService._get_timetable_by_id(timetable_id)
        appointments = cls.get_appointments(timetable.from_, timetable.to)
        taken_appointments = await cls.get_taken_appoinments(timetable_id)
        return sorted(set(appointments).difference(taken_appointments))
    
    @classmethod
    async def add_appointment(cls, timetable_id: int, time_: datetime) -> None:
        timetable = await MainTimetableService._get_timetable_by_id(timetable_id)
        free_appointments = await cls.get_free_appointments(timetable_id)
        if time_ not in free_appointments:
            raise TimeAlreadyTakenException
        await cls.add(
            timetable_id=timetable.id,
            from_=time_,
            to=time_ + timedelta(minutes=30),
        )
    
    @classmethod
    async def delete_appointment(cls, appointment_id: int) -> None:
        query = delete(Appointment).where(Appointment.id == appointment_id)
        await cls._execute_and_commit(query)