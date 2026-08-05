from fastapi import Depends, HTTPException, Request, status
from redis.asyncio import Redis

from app.db.engine import get_session
from app.db.redis import get_redis

from .factories import create_short_url_service
from .services import ShortUrlService

RATE_LIMIT = 10
WINDOW_SECONDS = 60

async def get_short_url_service(
    session = Depends(get_session),
    redis = Depends(get_redis),
) -> ShortUrlService:
    return create_short_url_service(session, redis)

async def rate_limit_shorten(
    request: Request,
    redis: Redis = Depends(get_redis),
) -> None:
    client_ip = request.client.host if request.client else "unknown"
    key = f"reatelimit:shorten:{client_ip}"

    count = await redis.incr(key)

    if count == 1:
        await redis.expire(key, WINDOW_SECONDS)

    if count > RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas requisições. Tente novamente em instantes."
        )