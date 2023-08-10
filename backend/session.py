import os

import asyncpg


async def get_connection_pool():
    pool = await asyncpg.create_pool(os.environ.get("DATABASE_URL"))
    return pool
