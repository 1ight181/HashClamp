from dataclasses import dataclass

from app.domain.entities.user.types import UserCreateOptions


@dataclass(frozen=True)
class CreateUserCommand:
    username: str
    email: str
    password: str
    opts: UserCreateOptions
