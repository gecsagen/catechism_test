import os
import settings
import asyncpg


async def get_connection_pool():
    pool = await asyncpg.create_pool(settings.TEST_DATABASE_URL)
    yield pool
    await pool.close()
