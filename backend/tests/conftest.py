import asyncpg
import asyncio
import settings
from typing import Any
from typing import AsyncGenerator
from main import app
from session import get_connection_pool
from fastapi.testclient import TestClient
import pytest_asyncio

CLEAN_TABLES = [
    "Users",
]


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def _asyncpg_pool():
    pool = await asyncpg.create_pool(settings.TEST_DATABASE_URL)
    yield pool
    await pool.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def clear_database():
    async with asyncpg.create_pool(settings.TEST_DATABASE_URL) as pool:
        async with pool.acquire() as conn:
            for table_for_cleaning in CLEAN_TABLES:
                await conn.execute(f"TRUNCATE TABLE {table_for_cleaning} CASCADE;")


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator:
    """
    Create a new FastAPI TestClient that uses the db_session fixture to override
    the get_db dependency that is injected into routes.
    """

    app.dependency_overrides[get_connection_pool] = _asyncpg_pool
    with TestClient(app) as client:
        yield client
