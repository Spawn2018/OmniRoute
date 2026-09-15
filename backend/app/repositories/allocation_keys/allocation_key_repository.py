from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.allocation_key import AllocationKey


def _key_query() -> Select[tuple[AllocationKey]]:
    return select(AllocationKey).order_by(AllocationKey.created_at.desc(), AllocationKey.id)


class AllocationKeyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[AllocationKey]:
        loaded = await self._session.scalars(_key_query())
        batch: Sequence[AllocationKey] = loaded.all()
        return list(batch)

    async def add(self, entity: AllocationKey) -> AllocationKey:
        self._session.add(entity)
        await self._session.flush()
        return entity
