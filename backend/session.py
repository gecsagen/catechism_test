import asyncpg


async def get_db():
    """Dependency for getting async session"""
    try:
        session = await asyncpg.connect("postgresql://postgres@localhost/test")
        yield session
    finally:
        await session.close()
