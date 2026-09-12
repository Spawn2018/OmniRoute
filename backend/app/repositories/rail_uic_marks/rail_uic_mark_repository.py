from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rail_uic_mark import RailUicMark


def _rail_uic_catalog_query() -> Select[tuple[RailUicMark]]:
    return select(RailUicMark).order_by(
        RailUicMark.mark_code.asc(),
        RailUicMark.created_at.desc(),
    )


class RailUicMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RailUicMark]:
        loaded = await self._session.scalars(_rail_uic_catalog_query())
        batch: Sequence[RailUicMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: RailUicMark) -> RailUicMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
