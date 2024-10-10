from fastapi import Depends, Request
import httpx

from timetable.app.exceptions import ForbiddenException, NotAuthenticatedException
from timetable.app.config import settings


async def get_validated_token(request: Request) -> dict | None:
    access_token = request.cookies.get('simbir-health-access-token')
    token_response = httpx.get(f'{settings.BASE_AUTH_URL}/Validate?accessToken={access_token}')
    token_response_json = token_response.json()
    if token_response_json.get('sub') is not None:
        return token_response_json
    

async def check_token(token_data: dict | None = Depends(get_validated_token)) -> None:
    if token_data is None:
        raise NotAuthenticatedException
    elif token_data.get('detail') == 'Токен отсутствует.':
        raise NotAuthenticatedException

class TokenRolesChecker:
    def __init__(self, roles: list[str] | None = None):
        if roles is None:
            self.roles = ['User'] # роль, присваиваемая пользователю по умолчанию
        else:
            self.roles = roles

    def __call__(self, token_data: dict = Depends(get_validated_token),  _ = Depends(check_token)):
        if token_data.get('roles') is None:
            raise ForbiddenException
        if not any(role in token_data.get('roles') for role in self.roles):
            raise ForbiddenException
        return self.roles
    

check_admin_or_manager = TokenRolesChecker(['Admin', 'Manager'])
check_admin_manager_or_doctor = TokenRolesChecker(['Admin', 'Manager', 'Doctor'])

        