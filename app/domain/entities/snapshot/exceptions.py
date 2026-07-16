class SnapshotDomainError(Exception):
    """Base exception for file entry domain errors."""


class InvalidSnapshotDataError(SnapshotDomainError):
    """Raised when file entry creation violates domain invariants."""


class InvalidSnapshotUpdateError(SnapshotDomainError):
    """Raised when file entry update violates domain invariants."""