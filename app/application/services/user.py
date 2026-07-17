from uuid import UUID

from app.application.exceptions.not_found import UserNotFoundError
from app.domain.entities.user.models import User
from app.domain.repositories.user import UserRepository


class UserService:
    def __init__(
            self,
            repo: UserRepository,
    ):
        self._repo = repo

    async def get_user(self, user_id: UUID) -> User:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        return user





