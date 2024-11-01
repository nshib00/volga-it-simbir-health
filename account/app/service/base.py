from sqlalchemy import delete, insert, select, update
from account.app.database import async_sessionmaker


class BaseGetService:
    model = None

    @classmethod
    async def _get_result(cls, query):
        async with async_sessionmaker() as session:
            result = await session.execute(query)
        return result
    
    @classmethod
    async def find_all(cls, *filters, **kw_filters):
        query = select(cls.model).filter_by(**kw_filters).filter(*filters)
        result = await cls._get_result(query)
        return result.scalars().all()
    
    @classmethod
    async def find_one_or_none(cls, *filters, **kw_filters):
        query = select(cls.model).filter_by(**kw_filters).filter(*filters)
        result = await cls._get_result(query)
        return result.scalars().one_or_none()


class BaseAddService:       
    @classmethod
    async def add(cls, **data):
        query = insert(cls.model).values(**data)
        async with async_sessionmaker() as session:
            await session.execute(query)
            await session.commit()

    
class BaseUpdateService:
    @classmethod
    async def update_one(cls, user_id: int, **values):
        query = update(cls.model).where(cls.model.id == user_id).values(**values)
        async with async_sessionmaker() as session:
            await session.execute(query)
            await session.commit()


class BaseDeleteService:
    @classmethod
    async def delete_one(cls, user_id: int):
        query = delete(cls.model).where(cls.model.id == user_id)
        async with async_sessionmaker() as session:
            await session.execute(query)
            await session.commit()

