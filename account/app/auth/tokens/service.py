from sqlalchemy import delete
from account.app.auth.tokens.models import RefreshToken
from account.app.service.base import BaseAddService, BaseDeleteService, BaseGetService
from account.app.database import async_sessionmaker


class RefreshTokenService(BaseAddService, BaseDeleteService, BaseGetService):
    model = RefreshToken

    @classmethod
    async def delete_by_value(cls, token_value: str):
        query = delete(cls.model).where(RefreshToken.value == token_value)
        async with async_sessionmaker() as session:
            await session.execute(query)
            await session.commit()