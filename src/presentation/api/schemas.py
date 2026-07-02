from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    user_id: str
    item_id: str
    quantity: int
    idempotency_key: str


class OrderResponse(BaseModel):
    id: str
    user_id: str
    item_id: str
    quantity: int
    status: str
    created_at: datetime
    updated_at: datetime


class PaymentCallbackRequest(BaseModel):
    payment_id: str
    order_id: str
    status: str
    amount: Decimal
    error_message: str | None = None
