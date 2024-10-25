from datetime import datetime
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy import ScalarResult

from document.app.checkers import (
    check_current_user, check_datetime_is_taken, check_history_datetime, check_history_input_data
)
from document.app.accounts import get_account_me
from document.app.dependencies import check_doctor_or_current_user, check_admin_manager_or_doctor
from document.elastic.service import ElasticService
from document.app.exceptions import ForbiddenException, HistoryNotExistsException
from document.app.schemas import HistoryResponseSchema, UserHistoryResponseSchema
from document.app.service import HistoryService


router = APIRouter(
    prefix='/api/History',
    tags=['История посещения и назначения']
)


@router.get('/Account/{pacientId}')
async def get_pacient_history(
    request: Request,
    pacientId: int,
    _ = Depends(check_doctor_or_current_user)
) -> list[UserHistoryResponseSchema]:
    check_current_user(pacientId, cookies=request.cookies)
    return await HistoryService.find_all(pacientId=pacientId)


@router.get('/{historyId}')
async def get_pacient_history_by_id(
    request: Request,
    historyId: int,
    _ = Depends(check_doctor_or_current_user)
) -> HistoryResponseSchema:
    history = await HistoryService.find_one_or_none(id=historyId)
    if history is None:
        raise HistoryNotExistsException
    current_user: dict = get_account_me(cookies=request.cookies)
    if 'User' in current_user.get('roles') and history.pacientId != current_user.get('id'):
        raise ForbiddenException
    return history


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_pacient_history(
    request: Request,
    date: datetime,
    pacientId: int,
    hospitalId: int,
    doctorId: int,
    room: str,
    data: str,
    _ = Depends(check_admin_manager_or_doctor)
) -> None:
    check_history_datetime(date)
    check_history_input_data(date, pacientId, hospitalId, doctorId, room, request.cookies)
    await check_datetime_is_taken(pacient_id=pacientId, datetime_to_check=date)
    new_history: ScalarResult = await HistoryService.add(
        return_model=True,
        date=date,
        pacientId=pacientId,
        hospitalId=hospitalId,
        doctorId=doctorId,
        room=room,
        data=data
    )
    await ElasticService.add_document(
        elastic_client=request.app.state.elastic_client,
        data=new_history
    )
    return new_history


@router.put('/{historyId}')
async def update_pacient_history(
    request: Request,
    historyId: int,
    date: datetime,
    pacientId: int,
    hospitalId: int,
    doctorId: int,
    room: str,
    data: str,
    _ = Depends(check_admin_manager_or_doctor)
) -> None:
    check_history_datetime(date)
    check_history_input_data(date, pacientId, hospitalId, doctorId, room, request.cookies)
    updated_history = await HistoryService.update_one(
        model_id=historyId,
        return_model=True,
        date=date,
        pacientId=pacientId,
        hospitalId=hospitalId,
        doctorId=doctorId,
        room=room,
        data=data
    )
    await ElasticService.update_document(
        elastic_client=request.app.state.elastic_client,
        data=updated_history
    )


@router.post('/Search')
async def search_history_by_data(
    request: Request,
    dataQuery: str,
    pacientId: int | None = None,
    historyDate: datetime | None = None,
    hospitalId: int | None = None,
    doctorId: int | None = None,
    _ = Depends(check_admin_manager_or_doctor)
) -> None:
    search_result = await ElasticService.search_in_history(
        user_query=dataQuery,
        elastic_client=request.app.state.elastic_client,
        pacient_id=pacientId,
        date=historyDate,
        hospital_id=hospitalId,
        doctor_id=doctorId,
    )
    return search_result