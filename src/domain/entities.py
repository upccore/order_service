from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class OrderStatus(StrEnum):
    NEW = "NEW"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELLED = "CANCELLED"


@dataclass
class Order:
    id: str
    user_id: str
    item_id: str
    quantity: int
    status: OrderStatus
    idempotency_key: str
    created_at: datetime
    updated_at: datetime
