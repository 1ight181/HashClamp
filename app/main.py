from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.persistence.sqlalchemy.constraints.constraint_registry import ConstraintRegistry
from app.infrastructure.persistence.sqlalchemy.db import Database
from app.config import settings
from app.infrastructure.persistence.sqlalchemy.models.node import NodeModel
from app.infrastructure.persistence.sqlalchemy.models.root import RootModel
from app.infrastructure.persistence.sqlalchemy.models.snapshot import SnapshotModel
from app.infrastructure.persistence.sqlalchemy.models.snapshot_file import SnapshotFileModel
from app.infrastructure.persistence.sqlalchemy.models.user import UserModel


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

        registry = ConstraintRegistry(
            [
                UserModel,
                NodeModel,
                RootModel,
                SnapshotModel,
                SnapshotFileModel,
            ],
        )
        
        application.state.registry = registry

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