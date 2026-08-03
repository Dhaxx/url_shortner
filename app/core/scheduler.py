import asyncio
import logging

from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.v1.short_urls.services import ShortUrlService

from app.db.engine import engine
from app.db.redis import get_redis
from app.api.v1.short_urls.factories import create_short_url_service

logger = logging.getLogger(__name__)

async def sync_access_counters_job(interval: int = 300) -> None:
    while True:
        try:
            async with AsyncSession(engine) as session:
                service = create_short_url_service(
                    session=session,
                    redis=get_redis(),
                )

                await service.sync_access_counters()

        except asyncio.CancelledError:
            logger.info("Serviço de sincronização finalizado.")
            raise

        except Exception:
            logger.exception("Erro ao sincronizar contadores de acesso.")

        await asyncio.sleep(interval)