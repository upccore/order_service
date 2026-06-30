from abc import ABC, abstractmethod
from typing import AsyncContextManager

from src.application.ports.repositories import OrderRepository


class UnitOfWork(ABC):

    @abstractmethod
    def __call__(self) -> AsyncContextManager["UnitOfWorkContext"]: ...


class UnitOfWorkContext(ABC):

    @property
    @abstractmethod
    def orders(self) -> OrderRepository: ...

    @abstractmethod
    async def commit(self) -> None: ...
