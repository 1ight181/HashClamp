from dataclasses import dataclass

from app.domain.entities.user.types import UserUpdateOptions


@dataclass(frozen=True)
class UpdateUserCommand:
    changes: UserUpdateOptions
