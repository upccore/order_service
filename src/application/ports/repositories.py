from abc import ABC, abstractmethod

from src.domain.entities import Order, OrderStatus


class OrderRepository(ABC):

    @abstractmethod
    async def create(
        self,
        user_id: str,
        item_id: str,
        quantity: int,
        idempotency_key: str,
    ) -> Order: ...

    @abstractmethod
    async def get_by_id(self, order_id: str) -> Order | None: ...

    @abstractmethod
    async def get_by_idempotency_key(self, key: str) -> Order | None: ...

    @abstractmethod
    async def update_status(self, order_id: str, status: OrderStatus) -> Order: ...
