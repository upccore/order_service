import asyncio
import logging

import httpx

from src.application.ports.notifications_client import NotificationsClient
from src.settings import settings

logger = logging.getLogger(__name__)

MAX_SEND_RETRIES = 3
RETRY_DELAY_SECONDS = 1.0


class HttpNotificationsClient(NotificationsClient):

    async def send(self, message: str, reference_id: str, idempotency_key: str) -> None:
        for attempt in range(1, MAX_SEND_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        f"{settings.notifications_base_url}/api/notifications",
                        headers={"X-API-Key": settings.notifications_api_key},
                        json={
                            "message": message,
                            "reference_id": reference_id,
                            "idempotency_key": idempotency_key,
                        },
                    )
                    response.raise_for_status()
                return
            except httpx.HTTPError:
                if attempt == MAX_SEND_RETRIES:
                    logger.exception(
                        "Failed to send notification for order %s after %d attempts",
                        reference_id,
                        MAX_SEND_RETRIES,
                    )
                else:
                    await asyncio.sleep(RETRY_DELAY_SECONDS)
