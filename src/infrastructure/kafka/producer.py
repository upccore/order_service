import asyncio
import json
import logging
from typing import Any

from aiokafka import AIOKafkaProducer

from src.application.ports.event_publisher import EventPublisher
from src.settings import settings

logger = logging.getLogger(__name__)

MAX_START_RETRIES = 5
INITIAL_RETRY_DELAY_SECONDS = 1.0


class KafkaEventPublisher(EventPublisher):

    def __init__(self) -> None:
        self._producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers)

    async def start(self) -> None:
        delay = INITIAL_RETRY_DELAY_SECONDS
        for attempt in range(1, MAX_START_RETRIES + 1):
            try:
                await self._producer.start()
                return
            except Exception:
                logger.exception(
                    "Kafka producer failed to start (attempt %d/%d)",
                    attempt,
                    MAX_START_RETRIES,
                )
                if attempt == MAX_START_RETRIES:
                    raise
                await asyncio.sleep(delay)
                delay *= 2

    async def stop(self) -> None:
        await self._producer.stop()

    async def publish(self, topic: str, key: str, value: dict[str, Any]) -> None:
        await self._producer.send_and_wait(
            topic, value=json.dumps(value).encode("utf-8"), key=key.encode("utf-8")
        )
