import uuid
from typing import Any

import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.outbox import OutboxEvent
from src.application.ports.outbox import OutboxRepository as OutboxRepositoryPort
from src.infrastructure.persistence.models import OutboxEventModel


class OutboxRepository(OutboxRepositoryPort):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, event_type: str, payload: dict[str, Any]) -> None:
        model = OutboxEventModel(id=uuid.uuid4(), event_type=event_type, payload=payload)
        self._session.add(model)
        await self._session.flush()

    async def get_unpublished(self, limit: int = 100) -> list[OutboxEvent]:
        stmt = (
            select(OutboxEventModel)
            .where(OutboxEventModel.published_at.is_(None))
            .order_by(OutboxEventModel.created_at)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.scalars().all()]

    async def mark_published(self, event_id: str) -> None:
        stmt = (
            sa.update(OutboxEventModel)
            .where(OutboxEventModel.id == uuid.UUID(event_id))
            .values(published_at=sa.func.now())
        )
        await self._session.execute(stmt)

    @staticmethod
    def _to_entity(model: OutboxEventModel) -> OutboxEvent:
        return OutboxEvent(
            id=str(model.id),
            event_type=model.event_type,
            payload=model.payload,
            created_at=model.created_at,
            published_at=model.published_at,
        )
