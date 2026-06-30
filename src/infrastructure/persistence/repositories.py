import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.repositories import OrderRepository as OrderRepositoryPort
from src.domain.entities import Order, OrderStatus
from src.infrastructure.persistence.models import OrderModel


class OrderRepository(OrderRepositoryPort):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: str,
        item_id: str,
        quantity: int,
        idempotency_key: str,
    ) -> Order:
        model = OrderModel(
            id=uuid.uuid4(),
            user_id=user_id,
            item_id=item_id,
            quantity=quantity,
            status=OrderStatus.NEW,
            idempotency_key=idempotency_key,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, order_id: str) -> Order | None:
        result = await self._session.get(OrderModel, uuid.UUID(order_id))
        return self._to_entity(result) if result else None

    async def get_by_idempotency_key(self, key: str) -> Order | None:
        stmt = select(OrderModel).where(OrderModel.idempotency_key == key)
        result = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._to_entity(result) if result else None

    @staticmethod
    def _to_entity(model: OrderModel) -> Order:
        return Order(
            id=str(model.id),
            user_id=model.user_id,
            item_id=model.item_id,
            quantity=model.quantity,
            status=OrderStatus(model.status),
            idempotency_key=model.idempotency_key,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
