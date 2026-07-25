from app.domain.entities.exceptions import DomainInvalidDataError
from app.domain.entities.snapshot_file.models import SnapshotFile


class SnapshotFileInvalidDataError(DomainInvalidDataError):
    """Raised when file entry creation violates domain invariants."""
    def __init__(self, message: str):
        super().__init__(SnapshotFile, message)


