from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


def create_sqlalchemy_async_engine(
    database_dsn: str,
    **kwargs,
) -> AsyncEngine:
    return create_async_engine(
        database_dsn,
        **kwargs,
    )