from typing import Union
from uuid import UUID
from asyncpg import Pool
from schemas import User


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, connection_pool: Pool):
        self.connection_pool = connection_pool

    # Создание пользователя
    async def create_user(
        self, name: str, surname: str, email: str, password: str
    ) -> User:
        async with self.connection_pool.acquire() as con:
            result: User = await con.fetchrow(
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
            deleted_id_str: str = await con.fetchval(
                """
                UPDATE Users
                SET is_active = False
                WHERE user_id = $1 AND is_active = True
                RETURNING id;
                """,
                user_id,
            )
            deleted_id = UUID(deleted_id_str) if deleted_id_str else None
            return deleted_id

    # Получение пользователя по id
    async def get_user_by_id(self, user_id: UUID) -> User:
        async with self.connection_pool.acquire() as con:
            result: User = await con.fetchrow(
                """
                    SELECT * FROM Users WHERE id = $1
                    RETURNING id, name, surname, email, is_active, is_admin;
                    """,
                user_id,
            )
            if result is not None:
                return result

    # Получение пользователя по email
    async def get_user_by_email(self, email: str) -> User:
        async with self.connection_pool.acquire() as con:
            result: User = await con.fetchrow(
                """
                    SELECT * FROM Users WHERE email = $1
                    RETURNING id, name, surname, email, is_active, is_admin, hashed_password;
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
            updated_id_str: str = await con.fetchval(query, user_id, *kwargs.values())
            updated_id = UUID(updated_id_str) if updated_id_str else None
            return updated_id
