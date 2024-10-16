import httpx

from document.app.exceptions import APIExceptionWithContext
from document.app.config import settings


def get_account(url_from: str, cookies: dict[str, str]) -> dict:
    response = httpx.get(url_from, cookies=cookies)
    account = response.json()

    if not response.is_success:
        raise APIExceptionWithContext(
            status_code=response.status_code,
            context={
                'url': url_from,
                'detail': account.get('detail')
            }
        )
    return account


def get_account_me(cookies: dict[str, str]) -> dict:
    me_url = f'{settings.BASE_ACCOUNTS_URL}/Me'
    return get_account(me_url, cookies)


def get_pacient(pacient_id: int, cookies: dict[str, str]) -> dict:
    user_url = f'{settings.BASE_ACCOUNTS_URL}/{pacient_id}'
    return get_account(user_url, cookies)