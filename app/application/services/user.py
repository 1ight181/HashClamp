from uuid import UUID

from app.application.cmd.create_user import CreateUserCommand
from app.application.cmd.update_user import UpdateUserCommand
from app.shared.exceptions.not_found import UserNotFoundError
from app.domain.entities.user.models import User
from app.domain.repositories.user import UserRepository
from app.domain.security import PasswordHasher


class UserService:
    def __init__(
            self,
            repo: UserRepository,
            password_hasher: PasswordHasher,
    ):
        self._repo = repo
        self._password_hasher = password_hasher

    async def get_user(self, user_id: UUID) -> User:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        return user

    async def create_user(self, user: CreateUserCommand) -> User:
        password_hash = self._password_hasher.hash(user.password)

        new_user = User.create(
            username=user.username,
            email=user.email,
            password_hash=password_hash,
            **user.opts,
        )

        await self._repo.save(new_user)

        return new_user

    async def update_user(self, user_id: UUID, user: UpdateUserCommand) -> User:
        current_user = await self._repo.get_by_id(user_id)
        if not current_user:
            raise UserNotFoundError(user_id)

        current_user.update(**user.changes)

        await self._repo.save(current_user)

        return current_user

    async def delete_user(self, user_id: UUID):
        if not await self._repo.delete(user_id):
            raise UserNotFoundError(user_id)

    async def change_password(self, user_id: UUID, old_password: str, new_password: str):
        current_user = await self._repo.get_by_id(user_id)
        if not current_user:
            raise UserNotFoundError(user_id)

        self._password_hasher.verify(old_password, current_user.password_hash)

        new_password_hash = self._password_hasher.hash(new_password)

        current_user.change_password(new_password_hash)

        await self._repo.save(current_user)







