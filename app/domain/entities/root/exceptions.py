from app.domain.entities.exceptions import DomainInvalidDataError
from app.domain.entities.root.models import Root


class RootInvalidDataError(DomainInvalidDataError):
    """Raised when root creation violates domain invariants."""
    def __init__(self, message: str):
        super().__init__(Root, message)