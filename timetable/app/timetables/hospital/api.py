from datetime import datetime
from fastapi import APIRouter, Depends, Request, status

from timetable.app.dependencies import check_token, check_admin_or_manager, check_admin_manager_or_doctor
from timetable.app.timetables.checkers import check_if_hospital_exists
from timetable.app.timetables.models import Timetable
from timetable.app.timetables.service import TimetableHospitalService


router = APIRouter(
    prefix='/api/Timetable/Hospital',
    tags=['Расписание больниц']
)


@router.get('/{hospitalId}')
async def get_hospital_timetable(request: Request, hospitalId: int, from_: datetime, to: datetime, _ = Depends(check_token)):
    await check_if_hospital_exists(hospitalId, request.cookies)
    return await TimetableHospitalService.find_all_timetables(from_, to, Timetable.hospitalId == hospitalId)


@router.delete('/{hospitalId}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_hospital_timetable(request: Request, hospitalId: int, _ = Depends(check_admin_or_manager)) -> None:
    await check_if_hospital_exists(hospitalId, request.cookies)
    await TimetableHospitalService.delete_hospital_timetables(mode_id=hospitalId)


@router.get('/{hospitalId}/Room/{roomId}')
async def get_room_timetable(
    request: Request,
    hospitalId: int,
    roomId: int,
    from_: datetime,
    to: datetime,
    _ = Depends(check_admin_manager_or_doctor)
):
    await check_if_hospital_exists(hospitalId, cookies=request.cookies) 
    return await TimetableHospitalService.get_room_timetables(roomId, from_, to)
    

