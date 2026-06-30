from fastapi import APIRouter, Depends, HTTPException, status

from src.application.usecases.create_order import CreateOrderUseCase
from src.application.usecases.get_order import GetOrderUseCase
from src.domain.exceptions import InsufficientStockError, OrderNotFoundError
from src.presentation.api.dependencies import get_create_order_use_case, get_get_order_use_case
from src.presentation.api.schemas import CreateOrderRequest, OrderResponse

router = APIRouter(prefix="/api/orders")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
async def create_order(
    body: CreateOrderRequest,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
):
    try:
        order = await use_case(
            user_id=body.user_id,
            item_id=body.item_id,
            quantity=body.quantity,
            idempotency_key=body.idempotency_key,
        )
        return OrderResponse(**order.__dict__)
    except InsufficientStockError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    use_case: GetOrderUseCase = Depends(get_get_order_use_case),
):
    try:
        order = await use_case(order_id)
        return OrderResponse(**order.__dict__)
    except OrderNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
