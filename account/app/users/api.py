from fastapi import APIRouter, Depends, status

from account.app.auth.dependencies import get_current_admin, get_current_user
from account.app.auth.hash_password import HashPassword
from account.app.users.models import User
from account.app.users.schemas import ShowUserSchema
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
    roles: list[str],
    user: User = Depends(get_current_admin)
) -> ShowUserSchema:
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