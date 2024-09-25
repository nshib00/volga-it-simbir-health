from fastapi import APIRouter, Depends, Response, status

from account.app.auth.dependencies import get_current_user
from account.app.auth.hash_password import HashPassword
from account.app.auth.logic import (
    authenticate_user,
    clear_access_token,
    clear_refresh_token,
    create_access_and_refresh_tokens,
    get_data_from_token,
    save_access_token, save_refresh_token
)
from account.app.auth.tokens.info import TokenInfo
from account.app.auth.tokens.service import RefreshTokenService
from account.app.exceptions import InvalidCredentialsException, InvalidTokenForRefreshException, UserNotExistsException
from account.app.users.models import User
from account.app.users.service import UserService


router = APIRouter(
    prefix='/Authentication',
    tags=['Аутентификация']
)


@router.post('/SignUp', status_code=status.HTTP_201_CREATED)
async def sign_up_user(lastName: str, firstName: str, username: str, password: str):
    await UserService.add(
        firstName=firstName,
        lastName=lastName,
        username=username,
        hashed_password=HashPassword.get_password_hash(password),
    )
    

@router.post('/SignIn')
async def sign_in_user(response: Response, username: str, password: str):
    if not username or not password:
        raise InvalidCredentialsException
    authenticated_user = await authenticate_user(username, password)
    if authenticated_user is None:
        raise UserNotExistsException
    tokens = create_access_and_refresh_tokens(
        token_data={'sub': authenticated_user.id}
    )
    save_access_token(tokens.access_token, response)
    await save_refresh_token(tokens.refresh_token, user_id=authenticated_user.id)
    return tokens


@router.post('/SignOut')
async def sign_out_user(response: Response, user: User = Depends(get_current_user)):
    clear_access_token(response)
    await clear_refresh_token(user_id=user.id)


@router.get('/Validate')
async def validate_token(accessToken: str):
    return get_data_from_token(accessToken)


@router.post('/Refresh')
async def refresh_token(response: Response, refreshToken: str, user: User = Depends(get_current_user)) -> TokenInfo:
    refresh_token_from_db = await RefreshTokenService.find_one_or_none(value=refreshToken) 
    if refresh_token_from_db is None:
        raise InvalidTokenForRefreshException
    clear_access_token(response)
    await clear_refresh_token(user_id=user.id)
    tokens = create_access_and_refresh_tokens(
        token_data={'sub': user.id}
    )
    save_access_token(tokens.access_token, response)
    await save_refresh_token(tokens.refresh_token, user_id=user.id)
    return tokens



