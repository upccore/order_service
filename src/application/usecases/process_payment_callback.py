from src.application.ports.uow import UnitOfWork
from src.domain.entities import OrderStatus
from src.domain.exceptions import OrderNotFoundError

ORDER_PAID_EVENT_TYPE = "order.paid"


class ProcessPaymentCallbackUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, order_id: str, status: str) -> None:
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
