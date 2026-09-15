
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db

router = APIRouter(tags=["redirect"])


@router.get("/{short_code}", include_in_schema=False)
async def redirect_to_original(short_code: str, db: AsyncSession = Depends(get_db)):
    url = await crud.get_by_code(db, short_code)
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")

    # Fire-and-forget style increment; still awaited, but done after we know
    # the code is valid so a bad request never touches the write path.
    await crud.increment_click_count(db, short_code)

    # 307 preserves the request method; a short link should behave like a
    # transparent pointer rather than implying a permanent (301) move,
    # since the mapping can still be deleted/changed by its owner.
    return RedirectResponse(url=url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
