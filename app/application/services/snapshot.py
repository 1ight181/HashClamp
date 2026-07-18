from uuid import UUID

from app.application.exceptions.not_found import SnapshotNotFoundError
from app.domain.entities.snapshot.models import Snapshot
from app.domain.repositories.snapshot import SnapshotRepository

from shared.exceptions.already_exists import EntityAlreadyExistsError


class SnapshotService:
    def __init__(
        self,
        repo: SnapshotRepository,
    ):
        self._repo = repo

    async def get_snapshot(
        self,
        snapshot_id: UUID,
    ) -> Snapshot:
        snapshot = await self._repo.get_by_id(snapshot_id)

        if not snapshot:
            raise SnapshotNotFoundError(snapshot_id)

        return snapshot

    async def create_snapshot(
        self,
        snapshot: Snapshot,
    ) -> Snapshot:
        try:
            await self._repo.save(snapshot)
        except EntityAlreadyExistsError:
            raise

        return snapshot

    async def update_snapshot(
        self,
        snapshot: Snapshot,
    ) -> Snapshot:
        try:
            await self._repo.save(snapshot)
        except EntityAlreadyExistsError:
            raise

        return snapshot

    async def delete_snapshot(
        self,
        snapshot_id: UUID,
    ) -> None:
        if not await self._repo.delete(snapshot_id):
            raise SnapshotNotFoundError(snapshot_id)