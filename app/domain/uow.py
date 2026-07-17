from contextlib import asynccontextmanager
from typing import Protocol

class UnitOfWork(Protocol):
    @asynccontextmanager
    async def transaction(self): ...