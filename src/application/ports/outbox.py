from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class OutboxEvent:
    id: str
    event_type: str
    payload: dict[str, Any]
    created_at: datetime
    published_at: datetime | None


class OutboxRepository(ABC):

    @abstractmethod
    async def add(self, event_type: str, payload: dict[str, Any]) -> None: ...

    @abstractmethod
    async def get_unpublished(self, limit: int = 100) -> list[OutboxEvent]: ...

    @abstractmethod
    async def mark_published(self, event_id: str) -> None: ...
