from pathlib import Path
from typing import TypedDict


class RootUpdateOptions(TypedDict, total=False):
    path: Path
    alias: str
    scan_interval_minutes: int