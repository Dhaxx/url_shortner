from collections.abc import Iterable

from redis.asyncio import Redis

from app.core.settings import settings


class ShortUrlCache:
    PREFIX = 'short:'
    STATS_PREFIX = 'stats:'

    def __init__(self, redis: Redis):
        self.redis = redis

    async def save(
        self,
        code: str,
        url: str,
        ttl: int = settings.short_url_ttl_seconds,
    ) -> None:
        """
        Salva uma URL no Redis com tempo de expiração.
        """
        ttl = ttl or settings.short_url_ttl_seconds

        await self.redis.set(
            name=f"{self.PREFIX}{code}",
            value=url,
            ex=ttl
        )

        # Contador de acessos não expira, para que seja mantido mesmo após a expiração da URL
        await self.redis.set(
            name=f"{self.STATS_PREFIX}{code}",
            value=0
        )

    async def get(self, code:str) -> str | None:
        """
        Recupera a URL original a partir do código.
        """
        return await self.redis.get(f"{self.PREFIX}{code}")

    async def exists(self, code:str) -> bool:
        """
        Verifica se a chave existe no Redis.
        """
        return await self.redis.exists(f"{self.PREFIX}{code}") > 0

    async def delete(self, code: str) -> None:
        """
        Remove a URL do Redis.
        """
        await self.redis.delete(f"{self.PREFIX}{code}")

    async def delete_stats(self, codes: Iterable[str]) -> None:
        """
        Remove o contador de acessos.
        """
        keys = [f"{self.STATS_PREFIX}{code}" for code in codes]

        if keys:
            await self.redis.delete(*keys)

    async def increment_access_count(self, code: str) -> int:
        """
        Incrementa o contador de acessos.
        """
        return await self.redis.incr(f"{self.STATS_PREFIX}{code}")

    async def get_access_counters(self) -> dict[str, int]:
        """
        Obtém quantidade de acessos dos links já expirados
        """
        counters = {}

        async for key in self.redis.scan_iter(f"{self.STATS_PREFIX}*"):
            code = key.removeprefix(self.STATS_PREFIX)

            # Verifica se o link está ativo
            if await self.exists(code):
                continue

            access_count = await self.redis.get(key)

            if access_count is None:
                continue

            counters[code] = int(access_count)  

        return counters          

    async def ttl(self, code: str) -> int:
        return await self.redis.ttl(f"{self.PREFIX}{code}")