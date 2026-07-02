import json
from typing import Any

from aiokafka import AIOKafkaProducer

from src.application.ports.event_publisher import EventPublisher
from src.settings import settings


class KafkaEventPublisher(EventPublisher):

    def __init__(self) -> None:
        self._producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers)

    async def start(self) -> None:
        await self._producer.start()

    async def stop(self) -> None:
        await self._producer.stop()

    async def publish(self, topic: str, key: str, value: dict[str, Any]) -> None:
        await self._producer.send_and_wait(
            topic, value=json.dumps(value).encode("utf-8"), key=key.encode("utf-8")
        )
