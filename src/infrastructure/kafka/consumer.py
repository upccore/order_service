import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

from src.application.ports.uow import UnitOfWork
from src.application.usecases.process_shipment_event import ProcessShipmentEventUseCase
from src.infrastructure.http.notifications_client import HttpNotificationsClient
from src.settings import settings

logger = logging.getLogger(__name__)

SHIPMENT_EVENTS_TOPIC = "student_system-shipment.events"
INITIAL_RETRY_DELAY_SECONDS = 1.0
MAX_RETRY_DELAY_SECONDS = 30.0


async def run_shipment_consumer(uow: UnitOfWork) -> None:
    notifications = HttpNotificationsClient()
    use_case = ProcessShipmentEventUseCase(uow, notifications)
    delay = INITIAL_RETRY_DELAY_SECONDS

    while True:
        consumer = AIOKafkaConsumer(
            SHIPMENT_EVENTS_TOPIC,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id="order-service",
            enable_auto_commit=False,
        )
        try:
            await consumer.start()
            delay = INITIAL_RETRY_DELAY_SECONDS
            async for message in consumer:
                try:
                    event = json.loads(message.value.decode("utf-8"))
                    await use_case(
                        topic=message.topic,
                        partition=message.partition,
                        offset=message.offset,
                        event=event,
                    )
                except Exception:
                    logger.exception(
                        "Failed to process shipment event: %s", message.value
                    )
                    continue
                await consumer.commit()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception(
                "Shipment consumer connection failed, retrying in %.0fs", delay
            )
        finally:
            await consumer.stop()

        await asyncio.sleep(delay)
        delay = min(delay * 2, MAX_RETRY_DELAY_SECONDS)
