class FileEntryDomainError(Exception):
    """Base exception for file entry domain errors."""


class InvalidFileEntryDataError(FileEntryDomainError):
    """Raised when file entry creation violates domain invariants."""


class InvalidFileEntryUpdateError(FileEntryDomainError):
    """Raised when file entry update violates domain invariants."""