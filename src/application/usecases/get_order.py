from src.application.ports.uow import UnitOfWork
from src.domain.entities import Order
from src.domain.exceptions import OrderNotFoundError


class GetOrderUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, order_id: str) -> Order:
        async with self._uow() as ctx:
            order = await ctx.orders.get_by_id(order_id)
            if order is None:
                raise OrderNotFoundError(f"Order {order_id} not found")
            return order
