from src.application.ports.notifications_client import NotificationsClient
from src.application.ports.uow import UnitOfWork
from src.domain.entities import OrderStatus
from src.domain.exceptions import OrderNotFoundError

ORDER_PAID_EVENT_TYPE = "order.paid"
PAID_MESSAGE = "PAID: Ваш заказ успешно оплачен и готов к отправке"


class ProcessPaymentCallbackUseCase:
    def __init__(self, uow: UnitOfWork, notifications: NotificationsClient) -> None:
        self._uow = uow
        self._notifications = notifications

    async def __call__(
        self, order_id: str, status: str, error_message: str | None = None
    ) -> None:
        new_status = (
            OrderStatus.PAID if status == "succeeded" else OrderStatus.CANCELLED
        )

        async with self._uow() as ctx:
            order = await ctx.orders.get_by_id(order_id)
            if order is None:
                raise OrderNotFoundError(f"Order {order_id} not found")

            updated = await ctx.orders.transition_status(
                order_id, from_status=OrderStatus.NEW, to_status=new_status
            )
            if updated is None:
                return

            if new_status == OrderStatus.PAID:
                await ctx.outbox.add(
                    event_type=ORDER_PAID_EVENT_TYPE,
                    payload={
                        "order_id": updated.id,
                        "item_id": updated.item_id,
                        "quantity": updated.quantity,
                        "idempotency_key": updated.idempotency_key,
                    },
                )

            await ctx.commit()

        if new_status == OrderStatus.PAID:
            message = PAID_MESSAGE
        else:
            message = f"CANCELLED: Ваш заказ отменен. Причина: {error_message or 'ошибка оплаты'}"

        await self._notifications.send(
            message=message,
            reference_id=order_id,
            idempotency_key=f"{order_id}-{new_status.value.lower()}",
        )
