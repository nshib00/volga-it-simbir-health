from fastapi import APIRouter, Depends, status
from sqlalchemy import String

from account.app.auth.dependencies import get_current_admin, get_current_user, check_admin_manager_or_doctor
from account.app.auth.hash_password import HashPassword
from account.app.auth.logic import clear_refresh_token
from account.app.exceptions import PacientNotExistsException
from account.app.users.models import User
from account.app.users.schemas import ShowUserSchema, UserRoles
from account.app.users.service import UserService


router = APIRouter(
    prefix='/api/Accounts',
    tags=['Аккаунты']
) 


@router.get('/Me')
async def get_accounts_me(user: User = Depends(get_current_user)) -> ShowUserSchema:
    return await UserService.find_one_or_none(id=user.id)


@router.put('/Update')
async def update_account_me(
    firstName: str, lastName: str, password: str, user: User = Depends(get_current_user)
) -> None:
    updated_current_user = await UserService.update_one(
        user_id=user.id, 
        firstName=firstName,
        lastName=lastName,
        hashed_password=HashPassword.get_password_hash(password),
    )
    return updated_current_user


@router.get('/Pacients')
async def get_all_pacients(_: User = Depends(check_admin_manager_or_doctor)) -> list[ShowUserSchema]:
    user_role_filter = User.roles[0].cast(String).icontains('user')
    return await UserService.find_all(user_role_filter)


@router.get('/Pacients/{user_id}')
async def get_pacient_by_id(user_id: int, _: User = Depends(check_admin_manager_or_doctor)) -> ShowUserSchema:
    user_role_filter = User.roles[0].cast(String).icontains('user')
    pacient = await UserService.find_one_or_none(user_role_filter, id=user_id)
    if pacient is None:
        raise PacientNotExistsException
    return pacient


@router.get('/')
async def get_all_accounts(user: User = Depends(get_current_admin)) -> list[ShowUserSchema]:
    return await UserService.find_all()


@router.put('/{user_id}')
async def update_account(
    user_id: int,
    first_name: str,
    last_name: str,
    username: str,
    password: str,
    roles: list[UserRoles],
    _: User = Depends(get_current_admin)
) -> None:
    hashed_password = HashPassword.get_password_hash(password)
    if HashPassword.verify(password, hashed_password):
        await UserService.update_one(
            user_id=user_id,
            firstName=first_name,
            lastName=last_name,
            username=username,
            hashed_password=hashed_password,
            roles=roles,
        )


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(user_id: int, user: User = Depends(get_current_admin)) -> None:
    await UserService.delete_one(user_id)
    await clear_refresh_token(user_id)