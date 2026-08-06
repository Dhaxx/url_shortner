from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.settings import settings

match settings.sgbd_driver:
    case "sqlite":
        engine = create_async_engine(
            settings.db_url.replace(
                "sqlite:///",
                "sqlite+aiosqlite:///"
            ),
            echo=True,
        )

    case "postgresql":
        engine = create_async_engine(
            settings.db_url.replace(
                "postgresql://",
                "postgresql+asyncpg://"
            ),
            echo=True,
        )
        
    case _:
        raise ValueError(f"Unsupported SGBD driver: {settings.sgbd_driver}")

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session