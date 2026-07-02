from src.application.ports.notifications_client import NotificationsClient
from src.application.ports.uow import UnitOfWork
from src.domain.entities import OrderStatus

EVENT_STATUS_MAP = {
    "order.shipped": OrderStatus.SHIPPED,
    "order.cancelled": OrderStatus.CANCELLED,
}

SHIPPED_MESSAGE = "SHIPPED: Ваш заказ отправлен в доставку"


class ProcessShipmentEventUseCase:
    def __init__(self, uow: UnitOfWork, notifications: NotificationsClient) -> None:
        self._uow = uow
        self._notifications = notifications

    async def __call__(
        self, topic: str, partition: int, offset: int, event: dict
    ) -> None:
        new_status = EVENT_STATUS_MAP.get(event.get("event_type"))
        if new_status is None:
            return

        order_id = event["order_id"]

        async with self._uow() as ctx:
            is_new = await ctx.inbox.try_reserve(topic, partition, offset)
            if not is_new:
                return

            updated = await ctx.orders.transition_status(
                order_id, from_status=OrderStatus.PAID, to_status=new_status
            )
            await ctx.commit()

        if updated is None:
            return

        if new_status == OrderStatus.SHIPPED:
            message = SHIPPED_MESSAGE
        else:
            message = (
                f"CANCELLED: Ваш заказ отменен. Причина: {event.get('reason', '')}"
            )

        await self._notifications.send(
            message=message,
            reference_id=order_id,
            idempotency_key=f"{order_id}-{new_status.value.lower()}",
        )
