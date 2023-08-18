from typing import Union
from uuid import UUID
from fastapi import Depends
from fastapi import HTTPException
from starlette import status
from jose import JWTError
from .schemas import ShowUser
from .schemas import UserCreate
from .schemas import User
from .dals import UserDAL
from .hashing import Hasher
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from asyncpg import Pool
from session import get_connection_pool
import settings


#  создание пользователя
async def _create_new_user(body: UserCreate, connection_pool: Pool) -> ShowUser:
    user_dal = UserDAL(connection_pool)
    user = await user_dal.create_user(
        name=body.name,
        surname=body.surname,
        email=body.email,
        password=Hasher.get_password_hash(body.password),
    )
    return ShowUser(
        user_id=user["id"],
        name=user["name"],
        surname=user["surname"],
        email=user["email"],
        is_active=user["is_active"],
    )


#  удаление пользователя
async def _delete_user(user_id, pool: Pool) -> Union[UUID, None]:
    user_dal = UserDAL(pool)
    deleted_user_id = await user_dal.delete_user(
        user_id=user_id,
    )
    return deleted_user_id


#  получение пользователя
async def _get_user_by_id(user_id, pool: Pool) -> Union[ShowUser, None]:
    user_dal = UserDAL(pool)
    user = await user_dal.get_user_by_id(
        user_id=user_id,
    )
    if user is not None:
        return ShowUser(
            user_id=user["user_id"],
            name=user["name"],
            surname=user["surname"],
            email=user["email"],
            is_active=user["is_active"],
        )


#  получение пользователя по email для авторизации
async def _get_user_by_email_for_auth(email: str, pool: Pool) -> User:
    user_dal = UserDAL(pool)
    return await user_dal.get_user_by_email(email=email)


#  обновление пользователя
async def _update_user(
    updated_user_params: dict, user_id: UUID, pool: Pool
) -> Union[UUID, None]:
    user_dal = UserDAL(pool)
    updated_user_id = await user_dal.update_user(user_id=user_id, **updated_user_params)
    return updated_user_id


#  аутентификация пользователя
async def authenticate_user(email: str, password: str, pool: Pool) -> Union[User, None]:
    user = await _get_user_by_email_for_auth(email=email, pool=pool)
    if user is None:
        return
    if not Hasher.verify_password(password, user["hashed_password"]):
        return
    return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


#  получеение актуального пользователя из токена
async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), pool: Pool = Depends(get_connection_pool)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        print("username/email extracted is ", email)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user: User = await _get_user_by_email_for_auth(email=email, pool=pool)
    if user is None:
        raise credentials_exception
    return user


def check_user_permissions(target_user: User, current_user: User) -> bool:
    if target_user["id"] != current_user["id"] and current_user["is_admin"] == True:
        return True
    return False
