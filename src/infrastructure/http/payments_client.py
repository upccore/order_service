from decimal import Decimal

import httpx

from src.application.ports.payments_client import (
    PaymentCreationError,
    PaymentResponse,
    PaymentsClient,
)
from src.settings import settings


class HttpPaymentsClient(PaymentsClient):

    async def create_payment(
        self,
        order_id: str,
        amount: Decimal,
        callback_url: str,
        idempotency_key: str,
    ) -> PaymentResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.payments_base_url}/api/payments",
                    headers={"X-API-Key": settings.payments_api_key},
                    json={
                        "order_id": order_id,
                        "amount": str(amount),
                        "callback_url": callback_url,
                        "idempotency_key": idempotency_key,
                    },
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as e:
            raise PaymentCreationError(str(e)) from e

        return PaymentResponse(
            id=data["id"],
            order_id=data["order_id"],
            amount=Decimal(data["amount"]),
            status=data["status"],
        )
