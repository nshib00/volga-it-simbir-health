import httpx

from account.app.exceptions import GeneralAPIException
from timetable.app.exceptions import DoctorNotFoundException, HospitalNotFoundException
from timetable.app.config import settings


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