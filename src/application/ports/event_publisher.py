from abc import ABC, abstractmethod
from typing import Any


class EventPublisher(ABC):

    @abstractmethod
    async def publish(self, topic: str, key: str, value: dict[str, Any]) -> None: ...
