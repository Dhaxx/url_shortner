from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .generators import ShortCodeGenerator
from .models import ShortUrl


class ShortUrlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.generator = ShortCodeGenerator

    async def create(self, short_url: ShortUrl) -> ShortUrl:
        self.session.add(short_url)
        await self.session.commit()
        await self.session.refresh(short_url)

        return short_url

    async def exists_by_code(self, code: str) -> bool:
        statement = select(ShortUrl).where(
            ShortUrl.short_code == code
        )

        result = await self.session.exec(statement)

        return result.first() is not None

    async def _generate_unique_code(self) -> str:
        while True:
            code = self.generator.generate()

            if not await self.exists_by_code(code):
                return code

    async def update_access_counter(self, counters: dict[str: int]) -> None:
        if not counters:
            return
        
        statement = select(ShortUrl).where(
            ShortUrl.short_code.in_(counters.keys())
        )

        urls = (await self.session.exec(statement)).all()
        
        for url in urls:
            url.access_count = counters[url.short_code]

        await self.session.commit()

    async def delete(self, code: str) -> None:
        if not await self.exists_by_code(code):
            return

        statement = delete(ShortUrl).where(ShortUrl.short_code == code)

        await self.session.exec(statement)

        await self.session.commit()