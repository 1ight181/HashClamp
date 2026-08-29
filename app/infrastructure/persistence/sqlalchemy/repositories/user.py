from sqlalchemy import select

from app.domain.entities.user.models import User
from app.domain.repositories.user import UserRepository
from app.infrastructure.persistence.sqlalchemy.constraints.constraint_registry import ConstraintRegistry
from app.infrastructure.persistence.sqlalchemy.models.user import UserModel
from app.infrastructure.persistence.sqlalchemy.repositories.base import SqlAlchemyBaseRepository, T_orm, T_domain


class SqlAlchemyUserRepository(UserRepository, SqlAlchemyBaseRepository[User, UserModel]):
    def __init__(
        self,
        session,
        constraint_registry: ConstraintRegistry,
    ):
        super().__init__(
            session, UserModel,
            constraint_registry,
        )

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

    @staticmethod
    def _to_domain(orm: UserModel) -> User:
        return User.restore(
            id=orm.id,
            username=orm.username,
            email=orm.email,
            password_hash=orm.password_hash,
            fullname=orm.fullname,
            notification_email=orm.notification_email,
            should_notify_on_changes=orm.should_notify_on_changes,
            default_scan_interval_minutes=orm.default_scan_interval_minutes,
            max_nodes=orm.max_nodes,
            is_active=orm.is_active,
            is_superuser=orm.is_superuser,
        )

    @staticmethod
    def _from_domain(domain: User) -> UserModel:
        return UserModel(
            id=domain.id,
            username=domain.username,
            email=domain.email,
            password_hash=domain.password_hash,
            fullname=domain.fullname,
            notification_email=domain.notification_email,
            should_notify_on_changes=domain.should_notify_on_changes,
            default_scan_interval_minutes=domain.default_scan_interval_minutes,
            max_nodes=domain.max_nodes,
            is_active=domain.is_active,
            is_superuser=domain.is_superuser,
        )

    @staticmethod
    def _update_orm_from_domain(orm: UserModel, domain: User):
        orm.username = domain.username
        orm.email = domain.email

        orm.password_hash = domain.password_hash

        orm.fullname = domain.fullname

        orm.is_active = domain.is_active
        orm.is_superuser = domain.is_superuser

        orm.default_scan_interval_minutes = domain.default_scan_interval_minutes
        orm.max_nodes = domain.max_nodes
        orm.should_notify_on_changes = domain.should_notify_on_changes
        orm.notification_email = domain.notification_email


