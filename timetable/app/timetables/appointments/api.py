from datetime import datetime
from fastapi import APIRouter, Depends, status

from timetable.app.dependencies import check_token
from timetable.app.timetables.service import AppointmentService


router = APIRouter(
    prefix='/api/Timetable',
    tags=['Записи на прием']
)


@router.get('/{recordId}/Appointments')
async def get_free_appointments(recordId: int, _ = Depends(check_token)):
    return await AppointmentService.get_free_appointments(timetable_id=recordId)


@router.post('/{recordId}/Appointments')
async def make_appointment(recordId: int, time_: datetime, _ = Depends(check_token)) -> None:
    await AppointmentService.add_appointment(timetable_id=recordId, time_=time_)


@router.delete('/Appointment/{appointmentId}', status_code=status.HTTP_204_NO_CONTENT)
async def cancel_appointment(appointmentId: int) -> None:
    await AppointmentService.delete_appointment(appointmentId)