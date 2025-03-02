# repositories/interfaces.py

from abc import ABC, abstractmethod
from typing import Any


class Repository(ABC):
    @abstractmethod
    async def list(self) -> list[Any]:
        pass

    @abstractmethod
    async def get(self, uid: int) -> Any:
        pass

    @abstractmethod
    async def create(self, record: Any) -> Any:
        pass

    @abstractmethod
    async def update(self, uid: int, record: Any) -> Any:
        pass

    @abstractmethod
    async def delete(self, uid: int) -> None:
        pass
