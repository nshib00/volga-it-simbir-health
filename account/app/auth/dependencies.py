from datetime import datetime, timezone
from fastapi import Depends, Request
import jwt

from account.app.auth.logic import get_data_from_token
from account.app.exceptions import ForbiddenException, NoTokenException, TokenExpiredException, UserNotExistsException
from account.app.config import settings
from account.app.users.models import User
from account.app.users.service import UserService


def get_token(request: Request) -> str:
    token = request.cookies.get('simbir-health-access-token')
    if token is None:
        raise NoTokenException
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        payload = get_data_from_token(token)
    except jwt.PyJWTError:
        raise NoTokenException
    token_expiration: str | None = payload.get('exp')
    if token_expiration is None or int(token_expiration) < datetime.now(timezone.utc).timestamp():
        raise TokenExpiredException
    user_id: str | None = payload.get('sub')
    if user_id is None:
        raise UserNotExistsException
    user = await UserService.find_one_or_none(id=user_id)
    if user is None:
        raise UserNotExistsException
    return user


def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if 'admin' not in user.roles:
        raise ForbiddenException
    return user