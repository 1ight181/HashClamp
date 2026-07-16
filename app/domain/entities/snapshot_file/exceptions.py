class SnapshotFileDomainError(Exception):
    """Base exception for file entry domain errors."""


class InvalidSnapshotFileDataError(SnapshotFileDomainError):
    """Raised when file entry creation violates domain invariants."""


class InvalidSnapshotFileUpdateError(SnapshotFileDomainError):
    """Raised when file entry update violates domain invariants."""