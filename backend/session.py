import os

import asyncpg


async def get_db():
    """Dependency for getting async session"""
    try:
        session = await asyncpg.connect(os.environ.get("DATABASE_URL"))
        yield session
    finally:
        await session.close()
