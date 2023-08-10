from fastapi import APIRouter
from .schemas import UserCreate, ShowUser
from .services import _create_new_user
from session import get_connection_pool
from asyncpg import Pool
from fastapi import Depends
from fastapi import HTTPException
from logging import getLogger

logger = getLogger(__name__)

user_router = APIRouter()


#  создание нового пользователя
@user_router.post("/", response_model=ShowUser)
async def create_user(
    body: UserCreate, db: Pool = Depends(get_connection_pool)
) -> ShowUser:
    try:
        #  вызывается функция создания нового пользователя
        return await _create_new_user(body, db)
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
