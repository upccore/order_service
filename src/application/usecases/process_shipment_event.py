from src.application.ports.uow import UnitOfWork
from src.domain.entities import OrderStatus

EVENT_STATUS_MAP = {
    "order.shipped": OrderStatus.SHIPPED,
    "order.cancelled": OrderStatus.CANCELLED,
}


class ProcessShipmentEventUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(
        self, topic: str, partition: int, offset: int, event: dict
    ) -> None:
        new_status = EVENT_STATUS_MAP.get(event.get("event_type"))
        if new_status is None:
            return

        async with self._uow() as ctx:
            is_new = await ctx.inbox.try_reserve(topic, partition, offset)
            if not is_new:
                return

            await ctx.orders.transition_status(
                event["order_id"], from_status=OrderStatus.PAID, to_status=new_status
            )
            await ctx.commit()
