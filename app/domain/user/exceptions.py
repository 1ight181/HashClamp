class UserDomainError(Exception):
    """Base exception for user domain errors."""


class InvalidUserDataError(UserDomainError):
    """Raised when user creation violates domain invariants."""


class InvalidUserUpdateError(UserDomainError):
    """Raised when user update violates domain invariants."""