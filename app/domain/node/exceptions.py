class NodeDomainError(Exception):
    """Base exception for node domain errors."""


class InvalidNodeDataError(NodeDomainError):
    """Raised when node creation violates domain invariants."""


class InvalidNodeUpdateError(NodeDomainError):
    """Raised when node update violates domain invariants."""