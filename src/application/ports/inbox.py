from abc import ABC, abstractmethod


class InboxRepository(ABC):

    @abstractmethod
    async def try_reserve(self, topic: str, partition: int, offset: int) -> bool:
        """True — событие обрабатываем впервые. False — уже обработано, пропускаем."""
        ...
