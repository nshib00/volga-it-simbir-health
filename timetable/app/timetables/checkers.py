from datetime import datetime, timedelta
import httpx

from timetable.app.exceptions import GeneralAPIException
from timetable.app.exceptions import (
    DoctorNotFoundException, HospitalNotFoundException, TimetableDateToSmallerDateFromException,
    TimetableInvalidFromDatetimeException, TimetableInvalidToDatetimeException, TooBigDateIntervalException
)
from timetable.app.config import settings


class DateValidator:
    @staticmethod
    def convert_to_datetime(datetime_str: str) -> datetime:
        return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    
    @staticmethod
    def validate_dates(date_from: datetime, date_to: datetime, check_time_delta: bool = False) -> None:
        if date_from.minute % 30 != 0 or date_from.second != 0:
            raise TimetableInvalidFromDatetimeException
        if date_to.minute % 30 != 0 or date_to.second != 0:
            raise TimetableInvalidToDatetimeException
        if date_to <= date_from:
            raise TimetableDateToSmallerDateFromException
        if check_time_delta and date_to - date_from > timedelta(hours=12):
            raise TooBigDateIntervalException
        
    @classmethod 
    def get_validated_dates(
        cls,
        date_from: str | datetime,
        date_to: str | datetime,
        check_time_delta: bool = False
    ) -> tuple[datetime, datetime]:
        if isinstance(date_from, str):
            date_from = cls.convert_to_datetime(date_from)
        if isinstance(date_to, str):
            date_to = cls.convert_to_datetime(date_to)
        cls.validate_dates(date_from, date_to, check_time_delta)
        return date_from, date_to


async def check_if_doctor_exists(doctor_id: int, cookies: dict[str, str]) -> None:
    url = f'{settings.BASE_DOCTORS_URL}/{doctor_id}'
    doctor_response = httpx.get(url, cookies=cookies)
    if doctor_response.status_code == 404:
        raise DoctorNotFoundException
    elif not doctor_response.is_success:
        raise GeneralAPIException(
            status_code=doctor_response.status_code,
            context={
                'url': url,
                'detail': doctor_response.json().get('detail')
            }
        )


async def check_if_hospital_exists(hospital_id: int, cookies: dict[str, str]) -> None:
    url = f'{settings.BASE_HOSPITAL_URL}/{hospital_id}'
    hospital_response = httpx.get(url, cookies=cookies)
    if hospital_response.status_code == 404:
        raise HospitalNotFoundException
    elif not hospital_response.is_success:
        raise GeneralAPIException(
            status_code=hospital_response.status_code,
            context={
                'url': url,
                'detail': hospital_response.json().get('detail')
            }
        )