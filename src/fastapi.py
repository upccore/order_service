import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.infrastructure.kafka.consumer import run_shipment_consumer
from src.infrastructure.kafka.outbox_publisher import run_outbox_publisher
from src.infrastructure.kafka.producer import KafkaEventPublisher
from src.infrastructure.persistence.database import session_factory
from src.infrastructure.persistence.uow import UnitOfWork
from src.presentation.api.routes.orders import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    publisher = KafkaEventPublisher()
    await publisher.start()
    uow = UnitOfWork(session_factory)

    background_tasks = [
        asyncio.create_task(run_outbox_publisher(uow, publisher)),
        asyncio.create_task(run_shipment_consumer(uow)),
    ]

    yield

    for task in background_tasks:
        task.cancel()
    await asyncio.gather(*background_tasks, return_exceptions=True)
    await publisher.stop()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(orders_router)
    return app
