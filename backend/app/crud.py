
from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import URL

from app.utils import generate_short_code


class ShortCodeGenerationError(RuntimeError):
    """Raised when we fail to find a free short code after several attempts."""


async def get_by_code(db: AsyncSession, short_code: str) -> URL | None:
    result = await db.execute(select(URL).where(URL.short_code == short_code))
    return result.scalar_one_or_none()

        



async def code_exists(db: AsyncSession, short_code: str) -> bool:
    result = await db.execute(select(URL.id).where(URL.short_code == short_code).limit(1))
    return result.scalar_one_or_none() is not None


async def create_url(db: AsyncSession, original_url: str, custom_code: str | None) -> URL:
    if custom_code:
        url = URL(short_code=custom_code, original_url=original_url)
        db.add(url)
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            raise ValueError(f"Short code '{custom_code}' is already taken") from exc
        await db.refresh(url)
        return url

    for _ in range(settings.max_code_generation_attempts):
        candidate = generate_short_code(settings.short_code_length)
        url = URL(short_code=candidate, original_url=original_url)
        db.add(url)
        try:
            await db.commit()
        except IntegrityError:
            # Collision on the random code; roll back and try again.
            await db.rollback()
            continue
        await db.refresh(url)
        return url

    raise ShortCodeGenerationError(
        "Could not generate a unique short code after several attempts"
    )


async def increment_click_count(db: AsyncSession, short_code: str) -> None:
    """
    Atomic UPDATE ... SET click_count = click_count + 1.

    Doing the increment in SQL (rather than read-modify-write in Python)
    avoids lost updates when many redirects hit the same code concurrently.
    """
    await db.execute(
        update(URL).where(URL.short_code == short_code).values(click_count=URL.click_count + 1)
    )
    await db.commit()


async def list_urls(db: AsyncSession, limit: int, offset: int) -> tuple[list[URL], int]:
    total_result = await db.execute(select(func.count()).select_from(URL))
    total = total_result.scalar_one()

    result = await db.execute(
        select(URL).order_by(URL.created_at.desc()).limit(limit).offset(offset)
    )
    items = list(result.scalars().all())
    return items, total


async def delete_url(db: AsyncSession, short_code: str) -> bool:
    url = await get_by_code(db, short_code)
    if url is None:
        return False
    await db.delete(url)
    await db.commit()
    return True
