from fastapi import Depends, Request

from account.app.auth.logic import get_data_from_token, validate_token
from account.app.exceptions import ForbiddenException, NoTokenException, UserNotExistsException
from account.app.users.models import User
from account.app.users.service import UserService


def get_token(request: Request) -> str:
    token = request.cookies.get('simbir-health-access-token')
    if token is None:
        raise NoTokenException
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    validate_token(token)
    payload: dict = get_data_from_token(token)
    user_id = payload.get('sub')
    user = await UserService.find_one_or_none(id=user_id)
    if user is None:
        raise UserNotExistsException
    return user


def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if 'admin' not in user.roles:
        raise ForbiddenException
    return user