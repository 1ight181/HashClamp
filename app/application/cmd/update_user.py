from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class UpdateUserCommand:
    changes: dict[str, Any]
