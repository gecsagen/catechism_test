from logging import getLogger
from uuid import UUID

from asyncpg import Pool
from fastapi import APIRouter, Depends, HTTPException, status
from session import get_connection_pool

from .schemas import DeleteUserResponse, ShowUser, User, UserCreate
from .services import (
    _create_new_user,
    _delete_user,
    _get_user_by_id,
    check_user_permissions,
    get_current_user_from_token,
)

logger = getLogger(__name__)

user_router = APIRouter()


#  создание нового пользователя
@user_router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreate, db: Pool = Depends(get_connection_pool)
) -> ShowUser:
    try:
        #  вызывается функция создания нового пользователя
        return await _create_new_user(body, db)
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    db: Pool = Depends(get_connection_pool),
    current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if not check_user_permissions(
        target_user=user_for_deletion,
        current_user=current_user,
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


#  получение пользователя по id
@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID,
    db: Pool = Depends(get_connection_pool),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    #  вызывается функция получения пользователя по id
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user
