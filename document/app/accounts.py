import httpx

from document.app.exceptions import APIExceptionWithContext
from document.app.config import settings


def get_json_response(url_from: str, cookies: dict[str, str]) -> dict:
    response = httpx.get(url_from, cookies=cookies)
    response_json = response.json()

    if not response.is_success:
        raise APIExceptionWithContext(
            status_code=response.status_code,
            context={
                'url': url_from,
                'detail': response_json.get('detail')
            }
        )
    return response_json


def get_account_me(cookies: dict[str, str]) -> dict:
    me_url = f'{settings.BASE_ACCOUNTS_URL}/Me'
    return get_json_response(me_url, cookies)


def get_pacient(pacient_id: int, cookies: dict[str, str]) -> dict:
    user_url = f'{settings.BASE_ACCOUNTS_URL}/Pacients/{pacient_id}'
    return get_json_response(user_url, cookies)