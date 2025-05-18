from __future__ import annotations

from uuid import uuid4

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
