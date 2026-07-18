from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.user import UserService
from app.domain.repositories.user import UserRepository
from app.infrastructure.persistence.sqlalchemy.constraints.constraint_registry import ConstraintRegistry
from app.infrastructure.persistence.sqlalchemy.repositories.user import SqlAlchemyUserRepository
from app.presentation.http.v1.deps.constraints import get_constraint_registry
from app.presentation.http.v1.deps.session import get_session


def get_user_repo(
    session: AsyncSession = Depends(get_session),
    constraint_registry: ConstraintRegistry = Depends(get_constraint_registry),
) -> UserRepository:
    return SqlAlchemyUserRepository(session, constraint_registry)

def get_user_service(
    repo: UserRepository = Depends(get_user_repo),
):
    return UserService(repo)