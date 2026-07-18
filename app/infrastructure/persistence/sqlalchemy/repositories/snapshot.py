from pathlib import Path
from uuid import UUID

from sqlalchemy import select, func, insert

from app.domain.entities.snapshot.models import (
    Snapshot,
    SnapshotStatus,
)
from app.domain.entities.snapshot_file.models import SnapshotFile
from app.domain.repositories.snapshot import SnapshotRepository
from app.infrastructure.persistence.sqlalchemy.constraints.constraint_registry import ConstraintRegistry

from app.infrastructure.persistence.sqlalchemy.models.snapshot import (
    SnapshotModel,
)
from app.infrastructure.persistence.sqlalchemy.models.snapshot_file import (
    SnapshotFileModel,
)

from app.infrastructure.persistence.sqlalchemy.repositories.base import (
    SqlAlchemyBaseRepository,
)


def _snapshot_file_to_domain(
        orm: SnapshotFileModel,
) -> SnapshotFile:

    return SnapshotFile.restore(
        id=orm.id,
        snapshot_id=orm.snapshot_id,
        relative_path=Path(orm.relative_path),
        filename=orm.filename,
        file_size=orm.file_size,
        hash_base64=orm.hash_base64,
    )


class SqlAlchemySnapshotRepository(
    SnapshotRepository,
    SqlAlchemyBaseRepository[Snapshot, SnapshotModel],
):

    def __init__(
        self,
        session,
        constraint_registry: ConstraintRegistry,
    ):
        super().__init__(
            session,
            SnapshotModel,
            constraint_registry
        )


    async def get_by_status_by_root_id(
        self,
        status: SnapshotStatus,
        root_id: UUID,
    ) -> list[Snapshot]:

        result = await self.session.execute(
            select(self.orm_model)
            .where(
                self.orm_model.root_id == root_id,
                self.orm_model.status == status.value,
            )
        )

        return [
            self._to_domain(snapshot)
            for snapshot in result.scalars().all()
        ]


    async def get_all_by_root_id(
        self,
        root_id: UUID,
    ) -> list[Snapshot]:

        result = await self.session.execute(
            select(self.orm_model)
            .where(
                self.orm_model.root_id == root_id,
            )
            .order_by(
                self.orm_model.created_at.desc()
            )
        )

        return [
            self._to_domain(snapshot)
            for snapshot in result.scalars().all()
        ]


    async def get_latest_completed_by_root_id(
        self,
        root_id: UUID,
    ) -> Snapshot | None:

        result = await self.session.execute(
            select(self.orm_model)
            .where(
                self.orm_model.root_id == root_id,
                self.orm_model.status == SnapshotStatus.COMPLETED.value,
            )
            .order_by(
                self.orm_model.created_at.desc()
            )
            .limit(1)
        )

        snapshot = result.scalar_one_or_none()

        return (
            self._to_domain(snapshot)
            if snapshot
            else None
        )


    async def get_previous_completed_by_root_id(
        self,
        root_id: UUID,
    ) -> Snapshot | None:

        result = await self.session.execute(
            select(self.orm_model)
            .where(
                self.orm_model.root_id == root_id,
                self.orm_model.status == SnapshotStatus.COMPLETED.value,
            )
            .order_by(
                self.orm_model.created_at.desc()
            )
            .offset(1)
            .limit(1)
        )

        snapshot = result.scalar_one_or_none()

        return (
            self._to_domain(snapshot)
            if snapshot
            else None
        )


    async def save_snapshot_files(
        self,
        files: list[SnapshotFile],
    ) -> None:
        
        await self.session.execute(
            insert(SnapshotFileModel),
            [
                {
                    "snapshot_id": file.snapshot_id,
                    "relative_path": str(file.relative_path),
                    "filename": file.filename,
                    "file_size": file.file_size,
                    "hash_base64": file.hash_base64,
                }
                for file in files
            ]
        )

        await self.session.flush()


    async def get_all_snapshot_files_by_snapshot_id(
        self,
        snapshot_id: UUID,
    ) -> list[SnapshotFile]:

        result = await self.session.execute(
            select(SnapshotFileModel)
            .where(
                SnapshotFileModel.snapshot_id == snapshot_id
            )
        )

        return [
            _snapshot_file_to_domain(file)
            for file in result.scalars().all()
        ]


    async def get_files_count_by_snapshot_id(
        self,
        snapshot_id: UUID,
    ) -> int:

        result = await self.session.execute(
            select(
                func.count(SnapshotFileModel.id)
            )
            .where(
                SnapshotFileModel.snapshot_id == snapshot_id
            )
        )

        return result.scalar_one()


    def _to_domain(
        self,
        orm: SnapshotModel,
    ) -> Snapshot:

        return Snapshot.restore(
            id=orm.id,
            root_id=orm.root_id,
            status=SnapshotStatus(orm.status),
            created_at=orm.created_at,
        )

    def _update_orm_from_domain(
        self,
        orm: SnapshotModel,
        domain: Snapshot,
    ):
        orm.root_id = domain.root_id
        orm.status = domain.status.value
        orm.created_at = domain.created_at