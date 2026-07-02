from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class PaymentResponse:
    id: str
    order_id: str
    amount: Decimal
    status: str


class PaymentCreationError(Exception):
    """Не удалось создать платёж в Payments Service"""


class PaymentsClient(ABC):

    @abstractmethod
    async def create_payment(
        self,
        order_id: str,
        amount: Decimal,
        callback_url: str,
        idempotency_key: str,
    ) -> PaymentResponse: ...
