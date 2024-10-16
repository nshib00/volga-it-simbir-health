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
    if 'Admin' not in user.roles:
        raise ForbiddenException
    return user


class TokenRolesChecker:
    def __init__(self, roles: list[str] | None = None):
        if not roles:
            self.roles = ['User'] # роль, присваиваемая пользователю по умолчанию
        else:
            self.roles = roles

    def __call__(self, token: str = Depends(get_token)):
        token_data = get_data_from_token(token)
        if token_data.get('roles') is None:
            raise ForbiddenException
        if not any(role in token_data.get('roles') for role in self.roles):
            raise ForbiddenException
        return self.roles
    

check_admin_manager_or_doctor = TokenRolesChecker(['Admin', 'Manager', 'Doctor'])