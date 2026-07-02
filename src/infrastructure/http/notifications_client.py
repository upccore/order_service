import logging

import httpx

from src.application.ports.notifications_client import NotificationsClient
from src.settings import settings

logger = logging.getLogger(__name__)


class HttpNotificationsClient(NotificationsClient):

    async def send(self, message: str, reference_id: str, idempotency_key: str) -> None:
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
        except httpx.HTTPError:
            logger.exception("Failed to send notification for order %s", reference_id)
