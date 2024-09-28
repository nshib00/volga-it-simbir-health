from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi import Response
import jwt

from account.app.auth.tokens.info import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TokenInfo
from account.app.auth.tokens.service import RefreshTokenService
from account.app.config import settings
from account.app.exceptions import InvalidTokenTypeException, NoTokenException, TokenExpiredException, UserNotExistsException
from account.app.users.models import User
from account.app.users.service import UserService
from account.app.auth.hash_password import HashPassword


def create_token(token_data: dict, token_type: str) -> str:
    data_to_encode = token_data.copy()
    if token_type == ACCESS_TOKEN_TYPE:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    elif token_type == REFRESH_TOKEN_TYPE:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        data_to_encode |= {
            'jti': str(uuid4())
        }
    else:
        raise InvalidTokenTypeException
    data_to_encode |= {
        'exp': expire,
        'type': token_type
    }
    encoded_jwt = jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_access_and_refresh_tokens(user_id: int, user_roles: list[str]) -> TokenInfo:
    token_data = {
        'sub': user_id,
        'roles': ','.join(user_roles)
    }
    return TokenInfo(
        access_token=create_token(token_data, token_type=ACCESS_TOKEN_TYPE),
        refresh_token=create_token(token_data, token_type=REFRESH_TOKEN_TYPE),
    )


def save_access_token(access_token: str, response: Response) -> None:
    response.set_cookie('simbir-health-access-token', access_token)


async def save_refresh_token(refresh_token: str, user_id: int) -> None:
    await RefreshTokenService.add(
        user_id=user_id,
        value=refresh_token,
    )


def clear_access_token(response: Response) -> None:
    response.delete_cookie('simbir-health-access-token')


async def clear_refresh_token(user_id: int | None = None, value: str | None = None) -> None:
    if user_id is not None:
        await RefreshTokenService.delete_one(user_id=user_id)
    elif value is not None:
        await RefreshTokenService.delete_by_value(token_value=value)
    

async def authenticate_user(username: str, password: str) -> User | None:
    user = await UserService.find_one_or_none(username=username)
    if user is None:
        return None
    if not HashPassword.verify(password, user.hashed_password):
        return None
    return user


def validate_token(token: str) -> None:
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
    return payload
    

def get_data_from_token(token: str) -> dict:
    return jwt.decode(
        token,
        key=settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    

