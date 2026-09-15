from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.allocation_level import AllocationLevel


def _key_query() -> Select[tuple[AllocationLevel]]:
    return select(AllocationLevel).order_by(AllocationLevel.created_at.desc(), AllocationLevel.id)


class AllocationLevelRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[AllocationLevel]:
        loaded = await self._session.scalars(_key_query())
        batch: Sequence[AllocationLevel] = loaded.all()
        return list(batch)

    async def add(self, entity: AllocationLevel) -> AllocationLevel:
        self._session.add(entity)
        await self._session.flush()
        return entity
