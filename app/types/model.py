from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    from ..extensions import db

    Model = db.Model

__all__ = ['Model']
