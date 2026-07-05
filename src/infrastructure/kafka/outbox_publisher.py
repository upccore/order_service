import asyncio
import logging

from src.application.ports.event_publisher import EventPublisher
from src.application.ports.notifications_client import NotificationsClient
from src.application.ports.uow import UnitOfWork

logger = logging.getLogger(__name__)

ORDER_EVENTS_TOPIC = "student_system-order.events"
NOTIFICATION_EVENT_TYPES = {"notification.new", "notification.cancelled"}
POLL_INTERVAL_SECONDS = 2


async def run_outbox_publisher(
    uow: UnitOfWork, publisher: EventPublisher, notifications: NotificationsClient
) -> None:
    while True:
        try:
            async with uow() as ctx:
                events = await ctx.outbox.get_unpublished()
                for event in events:
                    if event.event_type in NOTIFICATION_EVENT_TYPES:
                        await notifications.send(
                            message=event.payload["message"],
                            reference_id=event.payload["reference_id"],
                            idempotency_key=event.payload["idempotency_key"],
                        )
                    else:
                        value = {"event_type": event.event_type, **event.payload}
                        await publisher.publish(
                            topic=ORDER_EVENTS_TOPIC,
                            key=str(event.payload.get("order_id", event.id)),
                            value=value,
                        )
                    await ctx.outbox.mark_published(event.id)
                await ctx.commit()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("Failed to publish outbox events")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
