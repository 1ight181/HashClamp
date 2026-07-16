class RootDomainError(Exception):
    """Base exception for root domain errors."""


class InvalidRootDataError(RootDomainError):
    """Raised when root creation violates domain invariants."""


class InvalidRootUpdateError(RootDomainError):
    """Raised when root update violates domain invariants."""