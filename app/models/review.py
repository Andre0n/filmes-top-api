from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..types.model import Model

if TYPE_CHECKING:
    from .movie import Movie
    from .user import User


class Review(Model):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
    movie_id: Mapped[str] = mapped_column(
        ForeignKey('movies.id'), nullable=False
    )
    rating: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)

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

    user: Mapped[User] = relationship('User', back_populates='reviews')
    movie: Mapped[Movie] = relationship('Movie', back_populates='reviews')
