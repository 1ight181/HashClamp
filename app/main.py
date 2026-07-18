from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.persistence.sqlalchemy.db import Database
from app.config import settings


@asynccontextmanager
async def lifespan(
    application: FastAPI,
):
    database = None

    try:
        database = Database(
            config=settings.db_settings,
        )

        await database.health_check()

        application.state.database = database

        yield

    except Exception:
        # TODO: добавить логирование
        raise

    finally:
        if database is not None:
            await database.dispose()


app = FastAPI(
    lifespan=lifespan,
)