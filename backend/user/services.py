from typing import Union
from uuid import UUID
from fastapi import Depends
from fastapi import HTTPException
from starlette import status
from jose import JWTError
import settings
from .schemas import ShowUser
from .schemas import UserCreate
from .dals import UserDAL
from .hashing import Hasher
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from asyncpg import Pool


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
