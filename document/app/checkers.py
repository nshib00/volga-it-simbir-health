from datetime import datetime
from fastapi import status
import httpx

from document.app.accounts import get_account_me
from document.app.exceptions import (
    APIExceptionWithContext, DatetimeIsAlreadyTakenException, ForbiddenException, FutureDatetimeException, 
    HistoryInvalidDatetimeException, HospitalNotFoundException, RoomNotExistException, UserIsNotPacientOrDoctorException
)
from document.app.config import settings
from document.app.service import HistoryService


def check_history_input_data(
        date: datetime,
        pacientId: int,
        hospitalId: int,
        doctorId: int,
        room: int,
        user_cookies: dict[str, str]
    ) -> None:
    check_datetime_is_not_future(checking_datetime=date)
    check_if_pacient_exists(pacient_id=pacientId, cookies=user_cookies)
    check_if_hospital_exists(hospital_id=hospitalId, cookies=user_cookies)
    check_if_doctor_exists(doctor_id=doctorId, cookies=user_cookies)
    check_if_room_in_hospital_exists(room=room, hospital_id=hospitalId, cookies=user_cookies)


def check_datetime_is_not_future(checking_datetime: datetime) -> None:
    if checking_datetime > datetime.now():
        raise FutureDatetimeException
    

def check_if_object_exists(user_cookies: dict[str, str], url: str, error_404_detail_text: str) -> None:
    response = httpx.get(url, cookies=user_cookies)
    if response.status_code == status.HTTP_404_NOT_FOUND:
        exception_detail = error_404_detail_text
    elif not response.is_success:
        exception_detail = response.json().get('detail')
    else:
        return
    raise APIExceptionWithContext(
        status_code=response.status_code,
        context={
            'url': url,
            'detail': exception_detail
        }
    )


def check_current_user(user_id_to_check: int, cookies: dict[str, str]) -> None:
    '''
    Проверяет роль пользователя с id=user_id_to_check (является он доктором/пациентом или нет).
    Если пользователь - пациент, то также выполняется проверка, является ли он текущим пользователем
    (тем, кто залогинен прямо сейчас).
    '''
    pacient = get_account_me(cookies=cookies)
    pacient_roles = pacient.get('roles')
    if 'User' in pacient_roles: # проверка на то, является ли пользователь пациентом
        if user_id_to_check != pacient.get('id'):
            raise ForbiddenException
    else:
        check_if_pacient_exists(pacient_id=user_id_to_check, cookies=cookies)
        if 'Doctor' not in pacient_roles:
            raise UserIsNotPacientOrDoctorException

    
def check_if_pacient_exists(pacient_id: int, cookies: dict[str, str]) -> None:
    '''
    Проверяет, есть ли в базе данных пациент с id=pacient_id.
    '''
    url = settings.BASE_ACCOUNTS_URL + f'/Pacients/{pacient_id}'
    check_if_object_exists(
        url=url,
        user_cookies=cookies,
        error_404_detail_text='Пользователь с переданными данными либо не существует, либо не является пациентом.'
    )


def check_if_doctor_exists(doctor_id: int, cookies: dict[str, str]) -> None:
    check_if_object_exists(
        url=f'{settings.BASE_DOCTORS_URL}/{doctor_id}',
        user_cookies=cookies,
        error_404_detail_text='Такого доктора нет в системе.'
    )


def check_if_hospital_exists(hospital_id: int, cookies: dict[str, str]) -> None:
    url = f'{settings.BASE_HOSPITAL_URL}/{hospital_id}'
    hospital_response = httpx.get(url, cookies=cookies)
    if hospital_response.status_code == 404:
        raise HospitalNotFoundException
    elif not hospital_response.is_success:
        raise APIExceptionWithContext(
            status_code=hospital_response.status_code,
            context={
                'url': url,
                'detail': hospital_response.json().get('detail')
            }
        )
    

def check_if_room_in_hospital_exists(room: str, hospital_id: int, cookies: dict[str, str]) -> None:
    rooms_url = f'{settings.BASE_HOSPITAL_URL}/{hospital_id}/Rooms'
    rooms_response = httpx.get(rooms_url, cookies=cookies)
    if not rooms_response.is_success:
        raise APIExceptionWithContext(
            status_code=rooms_response.status_code,
            context={
                'url': rooms_url,
                'detail': rooms_response.json().get('detail')
            }
        )
    if room not in rooms_response.json():
        raise RoomNotExistException(room)
    

def check_history_datetime(history_datetime: datetime) -> None:
    if history_datetime.minute % 30 != 0 or history_datetime.second != 0:
        raise HistoryInvalidDatetimeException
    

async def check_datetime_is_taken(pacient_id: int, datetime_to_check: datetime):
    '''
    Если происходит попытка сделать запись в истории одного пользователя дважды на одно и то же время, возвращается ошибка. 
    '''
    history = await HistoryService.get_history_by_datetime(pacient_id, datetime_to_check)
    if history is not None:
        raise DatetimeIsAlreadyTakenException