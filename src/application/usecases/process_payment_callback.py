from src.application.ports.uow import UnitOfWork
from src.domain.entities import OrderStatus
from src.domain.exceptions import OrderNotFoundError


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
            if updated is not None:
                await ctx.commit()
