from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.multi_manning_mark import MultiManningMark


def _manning_catalog_query() -> Select[tuple[MultiManningMark]]:
    return select(MultiManningMark).order_by(
        MultiManningMark.mark_code.asc(),
        MultiManningMark.created_at.desc(),
    )


class MultiManningMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[MultiManningMark]:
        loaded = await self._session.scalars(_manning_catalog_query())
        batch: Sequence[MultiManningMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: MultiManningMark) -> MultiManningMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
