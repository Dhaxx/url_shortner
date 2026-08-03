from fastapi import FastAPI
from app.db.engine import create_db_and_tables
from app.db.redis import redis
from app.core.settings import settings

from contextlib import asynccontextmanager
import asyncio

from app.db.redis import get_redis
from app.api.v1.short_urls.router import router as short_urls_router

from app.core.scheduler import sync_access_counters_job
from app.api.v1.short_urls.dependencies import get_short_url_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")

    await create_db_and_tables()

    task = asyncio.create_task(sync_access_counters_job())

    yield

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass

    await redis.aclose()

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(short_urls_router, tags=["Short URLs"])