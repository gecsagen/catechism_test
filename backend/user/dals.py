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

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        async with self.connection_pool.acquire() as con:
            # Удаление записи и возврат id удаленной записи
            deleted_id: UUID = await con.fetchval(
                """
                UPDATE Users
                SET is_active = False
                WHERE user_id = $1 AND is_active = True
                RETURNING id;
                """,
                user_id,
            )
            return deleted_id

    # Получение пользователя по id
    async def get_user_by_id(self, user_id: UUID) -> Mapping[str, Any]:
        async with self.connection_pool.acquire() as con:
            result: Mapping[str, Any] = await con.fetchrow(
                """
                    SELECT * FROM Users WHERE id = $1
                    RETURNING id, name, surname, email, is_active, is_admin;
                    """,
                user_id,
            )
            if result is not None:
                return result

    # Получение пользователя по email
    async def get_user_by_email(self, email: str) -> Mapping[str, Any]:
        async with self.connection_pool.acquire() as con:
            result: Mapping[str, Any] = await con.fetchrow(
                """
                    SELECT * FROM Users WHERE email = $1
                    RETURNING id, name, surname, email, is_active, is_admin;
                    """,
                email,
            )
            if result is not None:
                return result

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        async with self.connection_pool.acquire() as con:
            # Формируем SET-часть запроса с помощью kwargs
            set_clause = ", ".join(
                [f"{field} = ${i+2}" for i, field in enumerate(kwargs)]
            )

            # Составляем и выполняем SQL-запрос
            query = f"""
                UPDATE Users
                SET {set_clause}
                WHERE user_id = $1 AND is_active = True
                RETURNING user_id;
            """
            updated_id = await con.fetchval(query, user_id, *kwargs.values())
            return updated_id
