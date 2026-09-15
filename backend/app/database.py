from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from collections.abc import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///./shortener.db"


engine = create_async_engine(
    url=DATABASE_URL,
    echo = False
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def init_db() -> None:
    """Creates tables on startup"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession | None]:
    """FastAPI dependency: yields a session and guarantees it is closed."""
    async with AsyncSessionLocal() as session:
        yield session


