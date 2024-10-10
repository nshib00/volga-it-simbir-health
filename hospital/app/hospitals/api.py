from fastapi import APIRouter, Depends

from hospital.app.exceptions import HospitalNotFoundException
from hospital.app.hospitals.dependencies import check_admin_token, check_token
from hospital.app.hospitals.schemas import HospitalResponseSchema
from hospital.app.hospitals.service import HospitalService


router = APIRouter(
    prefix='/api/Hospitals',
    tags=['Больницы']
)


@router.get('')
async def get_all_hospitals(
    from_: int | None = None, count: int | None = None,  _ = Depends(check_token)
) -> list[HospitalResponseSchema]:
    return await HospitalService.find_all(offset=from_, limit=count)
    
 
@router.get('/{hospital_id}')
async def get_hospital_by_id(hospital_id: int, _ = Depends(check_token)) -> HospitalResponseSchema:
    hospital = await HospitalService.find_one_or_none(id=hospital_id)
    if hospital is None:
        raise HospitalNotFoundException
    return hospital


@router.get('/{hospital_id}/Rooms')
async def get_hospital_rooms(hospital_id: int, _ = Depends(check_token)) -> list[dict | str]:
    hospital_rooms = await HospitalService.get_hospital_rooms(hospital_id)
    if hospital_rooms is None:
        raise HospitalNotFoundException
    return hospital_rooms
    

@router.post('')
async def add_new_hospital(
    name: str, address: str, contactPhone: str, rooms: list[str], _ = Depends(check_admin_token)
) -> None:
    await HospitalService.add(
        name=name,
        address=address,
        contactPhone=contactPhone,
        rooms=rooms,
    )


@router.put('/{hospital_id}')
async def update_hospital_data(
    hospital_id: int,
    name: str,
    address: str,
    contactPhone: str,
    rooms: list[str], _ = Depends(check_admin_token)
) -> None:
    await HospitalService.update_one(
        model_id=hospital_id,
        name=name,
        address=address,
        contactPhone=contactPhone,
        rooms=rooms,
    )


@router.delete('/{hospital_id}', status_code=204)
async def delete_hospital(hospital_id: int, _ = Depends(check_admin_token)) -> None:
    await HospitalService.delete_one(model_id=hospital_id)