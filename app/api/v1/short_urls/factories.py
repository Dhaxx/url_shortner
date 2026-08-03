from redis.asyncio import Redis
from sqlmodel.ext.asyncio.session import AsyncSession

from .cache import ShortUrlCache
from .repository import ShortUrlRepository
from .services import ShortUrlService

def create_short_url_service( session: AsyncSession, redis: Redis, ) -> ShortUrlService:
    repository = ShortUrlRepository(session)
    cache = ShortUrlCache(redis)

    return ShortUrlService(
        repository=repository,
        cache=cache,
    )