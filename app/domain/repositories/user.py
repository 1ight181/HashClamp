from typing import Protocol, Optional

from app.domain.repositories.base import BaseRepository
from app.domain.user.models import User


class UserRepository(BaseRepository[User]):
    async def get_by_email(self, email: str) -> Optional[User]: ...
    async def get_by_username(self, username: str) -> Optional[User]: ...

