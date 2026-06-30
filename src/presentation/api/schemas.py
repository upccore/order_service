from datetime import datetime

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
