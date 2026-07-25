from app.domain.entities.exceptions import DomainInvalidDataError
from app.domain.entities.snapshot.models import Snapshot


class SnapshotInvalidDataError(DomainInvalidDataError):
    """Raised when file entry creation violates domain invariants."""

    def __init__(self, message: str):
        super().__init__(Snapshot, message)

