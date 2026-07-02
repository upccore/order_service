import json
import logging

from aiokafka import AIOKafkaConsumer

from src.application.ports.uow import UnitOfWork
from src.application.usecases.process_shipment_event import ProcessShipmentEventUseCase
from src.settings import settings

logger = logging.getLogger(__name__)

SHIPMENT_EVENTS_TOPIC = "student_system-shipment.events"


async def run_shipment_consumer(uow: UnitOfWork) -> None:
    consumer = AIOKafkaConsumer(
        SHIPMENT_EVENTS_TOPIC,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id="order-service",
        enable_auto_commit=False,
    )
    use_case = ProcessShipmentEventUseCase(uow)

    await consumer.start()
    try:
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
                logger.exception("Failed to process shipment event: %s", message.value)
                continue
            await consumer.commit()
    finally:
        await consumer.stop()
