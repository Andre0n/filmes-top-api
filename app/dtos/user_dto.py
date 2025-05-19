from dataclasses import dataclass, field
from typing import Optional

from ..models import User


@dataclass
class UserDto:
    id: Optional[str] = field(default=None)
    username: str = field(default='')
    email: str = field(default='')
    name: str = field(default='')
    created_at: Optional[str] = field(default=None)
    updated_at: Optional[str] = field(default=None)

    @classmethod
    def from_model(cls, user: User) -> 'UserDto':
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
        )
