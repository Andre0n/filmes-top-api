from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:

    class Model(DeclarativeBase):
        __abstract__ = True

else:
    from ..extensions import db

    Model = db.Model

__all__ = ['Model']
