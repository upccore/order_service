from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.inbox import InboxRepository as InboxRepositoryPort
from src.infrastructure.persistence.models import InboxEventModel


class InboxRepository(InboxRepositoryPort):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def try_reserve(self, topic: str, partition: int, offset: int) -> bool:
        stmt = (
            pg_insert(InboxEventModel)
            .values(topic=topic, partition=partition, offset=offset)
            .on_conflict_do_nothing(index_elements=["topic", "partition", "offset"])
        )
        result = await self._session.execute(stmt)
        return result.rowcount > 0
