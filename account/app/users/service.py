from account.app.service.base import BaseAddService, BaseGetService, BaseUpdateService, BaseDeleteService
from account.app.users.models import User

class UserService(BaseGetService, BaseAddService, BaseUpdateService, BaseDeleteService):
    model = User

    @classmethod
    async def find_all_doctors(cls):
        return await UserService.find_all(roles='Doctor')

    @classmethod
    async def find_doctor_by_id(cls, doctor_id: int):
        return await BaseGetService.find_one_or_none(id=doctor_id, roles=['Doctor'])


    
            
