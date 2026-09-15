"""CRUD API routes, mounted under /api/urls."""
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.config import settings
from app.database import get_db
from app.models import URL
from app.schemas import URLCreateRequest, URLListReponse, URLResponse

router = APIRouter(prefix="/api/urls", tags=["urls"])


def _to_response(url: URL) -> URLResponse:
    return URLResponse(
        id=url.id,
        short_code=url.short_code,
        original_url=url.original_url,
        short_url=f"{settings.base_url.rstrip('/')}/{url.short_code}",
        click_count=url.click_count,
        created_at=url.created_at,
    )


@router.post("", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    request: Request,  # required positionally by slowapi's limiter decorator
    payload: URLCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> URLResponse:
    try:
        url = await crud.create_url(db, payload.original_url, payload.custom_code)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except crud.ShortCodeGenerationError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    return _to_response(url)


@router.get("", response_model=URLListReponse)
async def list_short_urls(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> URLListReponse:
    items, total = await crud.list_urls(db, limit=limit, offset=offset)
    return URLListReponse(
        items=[_to_response(u) for u in items],
        total=total,
        limit=limit,
        offset=offset,
    )





@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_short_url(short_code: str, db: AsyncSession = Depends(get_db)) -> None:
    deleted = await crud.delete_url(db, short_code)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
