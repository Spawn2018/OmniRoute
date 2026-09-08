from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity_event import EntityEvent


class EntityEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[EntityEvent]:
        result = await self._session.scalars(
            select(EntityEvent).order_by(EntityEvent.occurred_at.desc()),
        )
        return list(result.all())

    async def add(self, row: EntityEvent) -> EntityEvent:
        self._session.add(row)
        await self._session.flush()
        return row
