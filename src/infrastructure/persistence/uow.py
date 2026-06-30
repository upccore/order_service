from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.ports.uow import UnitOfWork as UnitOfWorkPort
from src.application.ports.uow import UnitOfWorkContext
from src.infrastructure.persistence.repositories import OrderRepository


class UnitOfWork(UnitOfWorkPort):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    @asynccontextmanager
    async def __call__(self):
        async with self._session_factory() as session:
            try:
                yield _UoWContext(session)
                await session.rollback()
            except Exception:
                await session.rollback()
                raise


class _UoWContext(UnitOfWorkContext):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._orders = OrderRepository(session)

    @property
    def orders(self) -> OrderRepository:
        return self._orders

    async def commit(self) -> None:
        await self._session.commit()
