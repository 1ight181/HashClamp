from app.domain.entities.exceptions import DomainInvalidDataError
from app.domain.entities.user.models import User


class UserInvalidDataError(DomainInvalidDataError):
    """Raised when user creation violates domain invariants."""
    def __init__(self, message: str):
        super().__init__(User, message)
