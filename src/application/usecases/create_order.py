from src.application.ports.catalog_client import CatalogClient
from src.application.ports.uow import UnitOfWork
from src.domain.entities import Order
from src.domain.exceptions import InsufficientStockError


class CreateOrderUseCase:
    def __init__(self, uow: UnitOfWork, catalog: CatalogClient) -> None:
        self._uow = uow
        self._catalog = catalog

    async def __call__(
        self,
        user_id: str,
        item_id: str,
        quantity: int,
        idempotency_key: str,
    ) -> Order:
        async with self._uow() as ctx:
            existing = await ctx.orders.get_by_idempotency_key(idempotency_key)
            if existing:
                return existing

        item = await self._catalog.get_item(item_id)
        if item.available_qty < quantity:
            raise InsufficientStockError(
                f"Available: {item.available_qty}, requested: {quantity}"
            )

        async with self._uow() as ctx:
            order = await ctx.orders.create(
                user_id=user_id,
                item_id=item_id,
                quantity=quantity,
                idempotency_key=idempotency_key,
            )
            await ctx.commit()
            return order
