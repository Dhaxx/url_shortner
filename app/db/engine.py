from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.settings import settings

if settings.sgbd_driver == "sqlite":
    engine = create_async_engine(
        settings.db_url.replace(
            "sqlite:///",
            "sqlite+aiosqlite:///"
        ),
        echo=True,
    )
else:
    engine = create_async_engine(
        settings.db_url.replace(
            "postgresql://",
            "postgresql+asyncpg://"
        ),
        echo=True,
        pool_size=20,
        max_overflow=40,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session