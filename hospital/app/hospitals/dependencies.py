from fastapi import Depends, Request
import httpx

from hospital.app.exceptions import ForbiddenException
from hospital.app.config import settings
from hospital.app.exceptions import NotAuthenticatedException


async def get_validated_token(request: Request) -> dict | None:
    access_token = request.cookies.get('simbir-health-access-token')
    token_response = httpx.get(f'{settings.BASE_AUTH_URL}/Validate?accessToken={access_token}')
    token_response_json = token_response.json()
    if token_response_json.get('sub') is not None:
        return token_response_json
    

async def check_token(token_data: dict = Depends(get_validated_token)) -> None:
    if token_data is None:
        raise NotAuthenticatedException
        

async def check_admin_token(token_data: dict = Depends(get_validated_token), _ = Depends(check_token)) -> None:
    if token_data.get('roles') is None or 'Admin' not in token_data.get('roles'):
        raise ForbiddenException