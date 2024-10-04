from fastapi import APIRouter, Depends, Request, status

from timetable.app.dependencies import check_token, check_admin_or_manager
from timetable.app.timetables.checkers import check_if_doctor_exists
from timetable.app.timetables.models import Timetable
from timetable.app.timetables.service import TimetableDoctorService


router = APIRouter(
    prefix='/api/Timetable/Doctor',
    tags=['Расписание врача']
)


@router.get('/{doctorId}')
async def get_doctor_timetable(request: Request, doctorId: int, from_: str, to: str, _ = Depends(check_token)):
    await check_if_doctor_exists(doctorId, request.cookies)
    return await TimetableDoctorService.find_all_timetables(from_, to, Timetable.doctorId == doctorId)


@router.delete('/{doctorId}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor_timetables(request: Request, doctorId: int, _ = Depends(check_admin_or_manager)) -> None:
    await check_if_doctor_exists(doctorId, request.cookies)
    await TimetableDoctorService.delete_doctor_timetables(doctor_id=doctorId)



