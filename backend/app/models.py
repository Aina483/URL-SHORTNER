"""ORM MODELS"""
from datetime import datetime, timezone

from sqlalchemy import DateTime, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

class URL(Base):
    __tablename__ = "url"

    id : Mapped[Integer] = mapped_column(Integer, primary_key = True, autoincrement = True)
    short_code : Mapped[str] = mapped_column(String(16), index = True, nullable = False, unique = True )
    original_url : Mapped[str] = mapped_column(String(2048), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)
    click_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    __table_args__ = (
            # Composite index to support "recent first" listing efficiently.
            Index("ix_urls_created_at_desc", created_at.desc()),
        )

