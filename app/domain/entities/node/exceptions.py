from app.domain.entities.exceptions import DomainInvalidDataError
from app.domain.entities.node.models import Node


class NodeInvalidDataError(DomainInvalidDataError):
    """Raised when node creation violates domain invariants."""
    def __init__(self, message: str):
        super().__init__(Node, message)

