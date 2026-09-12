from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.three_way_mark import ThreeWayMark


def _three_way_catalog_query() -> Select[tuple[ThreeWayMark]]:
    return select(ThreeWayMark).order_by(
        ThreeWayMark.mark_code.asc(),
        ThreeWayMark.created_at.desc(),
    )


class ThreeWayMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ThreeWayMark]:
        loaded = await self._session.scalars(_three_way_catalog_query())
        batch: Sequence[ThreeWayMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: ThreeWayMark) -> ThreeWayMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
