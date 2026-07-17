from collections.abc import AsyncGenerator

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.sqlalchemy.db import Database
from app.presentation.http.v1.deps.db import get_database


async def get_session(
    database: Database = Depends(get_database),
) -> AsyncGenerator[AsyncSession, None]:

    async with database.session_factory() as session:
        yield session