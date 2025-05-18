from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ..types.model import Model


class Movie(Model):
    __tablename__ = 'movies'

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4())
    )
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    year: Mapped[int] = mapped_column(
        nullable=False,
    )
    description: Mapped[str] = mapped_column(nullable=True)
    duration_minutes: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
