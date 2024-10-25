from sqlalchemy import ScalarResult, delete, insert, select, update
from document.app.database import async_sessionmaker


class BaseGetService:
    model = None

    @classmethod
    async def _get_result(cls, query):
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
        result = await cls._get_result(query)
        return result.scalars().all()
    
    @classmethod
    async def find_one_or_none(cls, **filters):
        query = select(cls.model).filter_by(**filters)
        result = await cls._get_result(query)
        return result.scalars().one_or_none()


class BaseAddService:     
    model = None

    @classmethod
    async def add(cls, return_model: bool = False, **data) -> ScalarResult | None:
        query = insert(cls.model).values(**data)
        if return_model:
            query = query.returning(cls.model)
        async with async_sessionmaker() as session:
            result = await session.execute(query)
            await session.commit()
        return result.scalar()

    
class BaseUpdateService:
    model = None

    @classmethod
    async def update_one(cls, model_id: int, return_model: bool = False, **values) -> ScalarResult | None:
        query = update(cls.model).where(cls.model.id == model_id).values(**values)
        if return_model:
            query = query.returning(cls.model)
        async with async_sessionmaker() as session:
            result = await session.execute(query)
            await session.commit()
        return result.scalar()


class BaseDeleteService:
    model = None

    @classmethod
    async def _execute_and_commit(cls, query) -> None:
        async with async_sessionmaker() as session:
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_one(cls, model_id: int):
        query = delete(cls.model).where(cls.model.id == model_id)
        await cls._execute_and_commit(query)
        