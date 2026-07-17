from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine


def create_sqlalchemy_async_session_factory(
    engine: AsyncEngine,
    **kwargs,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, **kwargs)