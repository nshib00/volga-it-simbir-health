from sqlalchemy import String, select
from account.app.users.models import User
from account.app.users.service import UserService


class DoctorService(UserService):
    model = User

    @classmethod
    def __get_doctors_query(cls, query_filter: str | None = None):
        if query_filter is not None:
            return select(cls.model).filter(
                User.roles[0].cast(String).icontains('doctor'),
                User.fullName.like(query_filter)
            )
        return select(cls.model).filter(
                User.roles[0].cast(String).icontains('doctor')
        )


    @classmethod
    async def find_all_doctors(
        cls, 
        limit: int | None = None,
        offset: int | None = None,
        filter_by: str | None = None
    ):
        query = cls.__get_doctors_query(query_filter=filter_by)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)    
        result = await cls._get_result(query)
        return result.scalars().all()
    

    @classmethod
    async def find_doctor_by_id(cls, doctor_id: int):
        query = cls.__get_doctors_query().filter_by(id=doctor_id)
        result = await cls._get_result(query)
        return result.scalars().one_or_none()