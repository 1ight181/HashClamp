from enum import Enum
from typing import TypedDict


class SnapshotStatus(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class SnapshotUpdateOptions(TypedDict, total=False):
    status: SnapshotStatus