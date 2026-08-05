from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse

from .dependencies import get_short_url_service
from .schemas import ShortenRequest, ShortenResponse
from .services import ShortUrlService

router = APIRouter(
    tags=["Short URLs"]
)

@router.post(
    "/shorten",
    response_model=ShortenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(
    request_data: ShortenRequest,
    request: Request,
    service: ShortUrlService = Depends(get_short_url_service)
):
    short_url = await service.create(request_data.url)

    return ShortenResponse(
        short_url=f"{request.base_url}{short_url.short_code}",
        expires_at=short_url.expires_at
    )

@router.get(
    "/{short_code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
)
async def redirect_short_url(
    short_code: str,
    service: ShortUrlService = Depends(get_short_url_service)
):
    return await service.redirect(short_code)