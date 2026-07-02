from abc import ABC, abstractmethod
from typing import AsyncContextManager

from src.application.ports.inbox import InboxRepository
from src.application.ports.outbox import OutboxRepository
from src.application.ports.repositories import OrderRepository


class UnitOfWork(ABC):

    @abstractmethod
    def __call__(self) -> AsyncContextManager["UnitOfWorkContext"]: ...


class UnitOfWorkContext(ABC):

    @property
    @abstractmethod
    def orders(self) -> OrderRepository: ...

    @property
    @abstractmethod
    def outbox(self) -> OutboxRepository: ...

    @property
    @abstractmethod
    def inbox(self) -> InboxRepository: ...

    @abstractmethod
    async def commit(self) -> None: ...
