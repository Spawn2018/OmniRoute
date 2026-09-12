from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rail_cim_mark import RailCimMark


def _csrd_catalog_query() -> Select[tuple[RailCimMark]]:
    return select(RailCimMark).order_by(RailCimMark.mark_code.asc(), RailCimMark.created_at.desc())


class RailCimMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RailCimMark]:
        loaded = await self._session.scalars(_csrd_catalog_query())
        batch: Sequence[RailCimMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: RailCimMark) -> RailCimMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
