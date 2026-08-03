from fastapi import Depends

from .services import ShortUrlService
from .repository import ShortUrlRepository
from .cache import ShortUrlCache

from app.db.engine import get_session
from app.db.redis import get_redis

from .factories import create_short_url_service

async def get_short_url_service(
    session = Depends(get_session),
    redis = Depends(get_redis),
) -> ShortUrlService:
    return create_short_url_service(session, redis)