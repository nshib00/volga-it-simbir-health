from sqlalchemy import String, select
from account.app.users.models import User
from account.app.users.service import UserService


class DoctorService(UserService):
    model = User

    @classmethod
    def __get_doctors_query(cls):
        return select(cls.model).filter(User.roles[0].cast(String).icontains('doctor'))


    @classmethod
    async def find_all_doctors(cls):
        query = cls.__get_doctors_query()
        result = await cls._get_result(query)
        return result.scalars().all()
    

    @classmethod
    async def find_doctor_by_id(cls, doctor_id: int):
        query = cls.__get_doctors_query().filter_by(id=doctor_id)
        result = await cls._get_result(query)
        return result.scalars().one_or_none()