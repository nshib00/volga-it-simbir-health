from datetime import datetime
from fastapi import APIRouter, Depends, Request, status

from timetable.app.dependencies import check_admin_or_manager
from timetable.app.timetables.checkers import check_if_doctor_exists, check_if_hospital_exists
from timetable.app.timetables.service import MainTimetableService

 
router = APIRouter(
    prefix='/api/Timetable',
    tags=['Расписание']
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_new_timetable_record(
    request: Request,
    hospitalId: int,
    doctorId: int,
    from_: datetime,
    to: datetime,
    room: str,
    _ = Depends(check_admin_or_manager)
) -> None:
    from_ = from_.replace(tzinfo=None)
    to = to.replace(tzinfo=None)
    await check_if_doctor_exists(doctorId, cookies=request.cookies) 
    await check_if_hospital_exists(hospitalId, cookies=request.cookies) 
    await MainTimetableService.add_timetable(
        hospitalId=hospitalId,
        doctorId=doctorId,
        from_=from_,
        to=to,
        room=room,
    )


@router.put('/{recordId}')
async def update_timetable_record(
    request: Request,
    recordId: int,
    hospitalId: int,
    doctorId: int,
    from_: datetime,
    to: datetime,
    room: str,
    _ = Depends(check_admin_or_manager)
) -> None:
    from_ = from_.replace(tzinfo=None)
    to = to.replace(tzinfo=None)
    await check_if_doctor_exists(doctorId, cookies=request.cookies) 
    await check_if_hospital_exists(hospitalId, cookies=request.cookies) 
    await MainTimetableService.update_timetable(
        timetableId=recordId,
        hospitalId=hospitalId,
        doctorId=doctorId,
        from_=from_,
        to=to,
        room=room,
    )


@router.delete('/{recordId}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_timetable_record(recordId: int, _ = Depends(check_admin_or_manager)) -> None:
    await MainTimetableService.delete_one(model_id=recordId)



