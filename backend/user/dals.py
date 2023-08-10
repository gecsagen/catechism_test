from typing import Union
from uuid import UUID
from asyncpg import Pool
from typing import Mapping, Any


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, connection_pool: Pool):
        self.connection_pool = connection_pool

    # Создание пользователя
    async def create_user(
        self, name: str, surname: str, email: str, password: str
    ) -> Mapping[str, Any]:
        async with self.connection_pool.acquire() as con:
            result: Mapping[str, Any] = await con.fetchrow(
                """
                INSERT INTO Users(name, surname, email, hashed_password)
                VALUES($1, $2, $3, $4)
                RETURNING id, name, surname, email, is_active;
                """,
                name,
                surname,
                email,
                password,
            )
            return result

    # Удаление пользователя
    async def delete_user(self, user_id: UUID) -> Union[int, None]:
        await self.db_session.execute(
            """
        DELETE From Users WHERE id = $user_id
        """,
            user_id,
        )

    # Получение пользователя по id
    async def get_user_by_id(self, user_id: UUID):
        await self.db_session.fetch(
            """
        SELECT * FROM Users WHERE id = $user_id
        """,
            user_id,
        )

    # Получение пользователя по email
    async def get_user_by_email(self, email: str):
        await self.db_session.fetch(
            """
        SELECT * FROM Users WHERE id = $email
        """,
            email,
        )

    # Обновление пользователя
    # async def update_user(self, user_id: int, **kwargs) -> Union[UUID, None]:
    #     query = (
    #         update(User)
    #         .where(and_(User.user_id == user_id, User.is_active == True))
    #         .values(kwargs)
    #         .returning(User.user_id)
    #     )
    #     await self.db_session.fetch(
    #     """
    #     UPDATE Users WHERE id = $user_id AND is_active = 1
    #     """,
    #         user_id
    #     )
