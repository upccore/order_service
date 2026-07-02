from src.application.ports.catalog_client import CatalogClient
from src.application.ports.payments_client import PaymentCreationError, PaymentsClient
from src.application.ports.uow import UnitOfWork
from src.domain.entities import Order, OrderStatus
from src.domain.exceptions import InsufficientStockError
from src.settings import settings


class CreateOrderUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        catalog: CatalogClient,
        payments: PaymentsClient,
    ) -> None:
        self._uow = uow
        self._catalog = catalog
        self._payments = payments

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

        callback_url = f"{settings.callback_base_url}/api/orders/payment-callback"
        try:
            await self._payments.create_payment(
                order_id=order.id,
                amount=item.price * quantity,
                callback_url=callback_url,
                idempotency_key=idempotency_key,
            )
        except PaymentCreationError:
            async with self._uow() as ctx:
                order = await ctx.orders.update_status(order.id, OrderStatus.CANCELLED)
                await ctx.commit()

        return order
