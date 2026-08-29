from pathlib import Path
from typing import TypedDict


class FileEntryUpdateOptions(TypedDict, total=False):
    relative_path: Path
    filename: str
    file_size: int
    hash_base64: str