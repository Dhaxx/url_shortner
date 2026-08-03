from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from .repository import ShortUrlRepository
from .cache import ShortUrlCache
from .models import ShortUrl

class ShortUrlService:
    def __init__(
        self,
        repository: ShortUrlRepository,
        cache: ShortUrlCache
    ):
        self.repository = repository
        self.cache = cache

    async def create(self, url: str) -> ShortUrl:
        code = await self.repository._generate_unique_code()

        url_str = str(url)

        short_url = ShortUrl(
            original_url=url_str,
            short_code=code
        )

        try:
            await self.repository.create(short_url)
            await self.cache.save(code, url_str)
        except Exception as e:
            print(e)
            await self.repository.delete(code)
            raise

        return short_url

    async def redirect(self, code: str) -> None:
        original_url = await self.cache.get(code)

        if original_url is None:
            raise HTTPException(
                status_code=410,
                detail="Link expirado ou inexistente."
            )

        await self.cache.increment_access_count(code)

        return RedirectResponse(
            url=original_url,
            status_code=302
        )

    async def sync_access_counters(self) -> None:
        counters = await self.cache.get_access_counters()

        if not counters:
            return

        await self.repository.update_access_counter(counters)

        await self.cache.delete_stats(counters.keys())