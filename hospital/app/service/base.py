from sqlalchemy import delete, insert, select, update
from hospital.app.database import async_sessionmaker


class BaseGetService:
    model = None

    @classmethod
    async def __get_result(cls, query):
        async with async_sessionmaker() as session:
            result = await session.execute(query)
        return result
    
    @classmethod
    async def find_all(cls, offset: int | None = None, limit: int | None = None, **filters):
        query = select(cls.model).filter_by(**filters)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await cls.__get_result(query)
        return result.scalars().all()
    
    @classmethod
    async def find_one_or_none(cls, **filters):
        query = select(cls.model).filter_by(**filters)
        result = await cls.__get_result(query)
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
    async def update_one(cls, model_id: int, **values):
        query = update(cls.model).where(cls.model.id == model_id).values(**values)
        async with async_sessionmaker() as session:
            await session.execute(query)
            await session.commit()


class BaseDeleteService:
    @classmethod
    async def delete_one(cls, model_id: int):
        query = delete(cls.model).where(cls.model.id == model_id)
        async with async_sessionmaker() as session:
            await session.execute(query)
            await session.commit()

