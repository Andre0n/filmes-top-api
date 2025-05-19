from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..types.model import Model

if TYPE_CHECKING:
    from .rental import Rental
    from .review import Review


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
    genre: Mapped[str] = mapped_column(nullable=False)
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

    rentals: Mapped[list[Rental]] = relationship(back_populates='movie')
    reviews: Mapped[list[Review]] = relationship(back_populates='movie')
