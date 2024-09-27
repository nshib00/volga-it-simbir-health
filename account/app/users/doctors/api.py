from fastapi import APIRouter, Depends

from account.app.auth.dependencies import get_current_user
from account.app.exceptions import DoctorNotExistsException
from account.app.users.doctors.service import DoctorService
from account.app.users.models import User
from account.app.users.schemas import ShowUserSchema


router = APIRouter(
    prefix='/api/Doctors',
    tags=['Доктора']
) 


@router.get('')
async def get_all_doctors(user: User = Depends(get_current_user)) -> list[ShowUserSchema]:
    return await DoctorService.find_all_doctors()


@router.get('/{doctor_id}')
async def get_doctor_by_id(doctor_id: int, user: User = Depends(get_current_user)) -> ShowUserSchema:
    doctor = await DoctorService.find_doctor_by_id(doctor_id=doctor_id)
    if doctor is None:
        raise DoctorNotExistsException
    return doctor