from sqlalchemy import select

from app.domain.entities.user.models import User
from app.domain.repositories.user import UserRepository
from app.infrastructure.persistence.sqlalchemy.models.user import UserModel
from app.infrastructure.persistence.sqlalchemy.repositories.base import SqlAlchemyBaseRepository


class SqlAlchemyUserRepository(UserRepository, SqlAlchemyBaseRepository[User, UserModel]):
    def __init__(self, session):
        super().__init__(session, UserModel)

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(self.orm_model).where(self.orm_model.username == username)
        )

        orm = result.scalar_one_or_none()

        return self._to_domain(orm) if orm else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(self.orm_model).where(self.orm_model.email == email)
        )

        orm = result.scalar_one_or_none()

        return self._to_domain(orm) if orm else None


    def _to_domain(self, user_orm: UserModel) -> User:
        return User.restore(
            id=user_orm.id,
            username=user_orm.username,
            email=user_orm.email,
            password_hash=user_orm.password_hash,
            fullname=user_orm.fullname,
            notification_email=user_orm.notification_email,
            should_notify_on_changes=user_orm.should_notify_on_changes,
            default_scan_interval_minutes=user_orm.default_scan_interval_minutes,
            max_nodes=user_orm.max_nodes,
            is_active=user_orm.is_active,
            is_superuser=user_orm.is_superuser,
        )

    def _update_orm_from_domain(self, orm: UserModel, domain: User):
        orm.id = domain.id
        orm.username = domain.username
        orm.email = domain.email
        orm.password_hash = domain.password_hash
        orm.fullname = domain.fullname
        orm.notification_email = domain.notification_email
        orm.should_notify_on_changes = domain.should_notify_on_changes
        orm.default_scan_interval_minutes = domain.default_scan_interval_minutes
        orm.max_nodes = domain.max_nodes
        orm.is_active = domain.is_active
        orm.is_superuser = domain.is_superuser
