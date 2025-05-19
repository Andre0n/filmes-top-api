from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..types.model import Model

if TYPE_CHECKING:
    from .movie import Movie
    from .user import User


class Rental(Model):
    __tablename__ = 'rentals'

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
    movie_id: Mapped[str] = mapped_column(
        ForeignKey('movies.id'), nullable=False
    )
    rented_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    user: Mapped[User] = relationship('User', back_populates='rentals')
    movie: Mapped[Movie] = relationship('Movie', back_populates='rentals')
