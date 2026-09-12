from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.line_impact_mark import LineImpactMark


def _line_impact_catalog_query() -> Select[tuple[LineImpactMark]]:
    return select(LineImpactMark).order_by(
        LineImpactMark.mark_code.asc(),
        LineImpactMark.created_at.desc(),
    )


class LineImpactMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[LineImpactMark]:
        loaded = await self._session.scalars(_line_impact_catalog_query())
        batch: Sequence[LineImpactMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: LineImpactMark) -> LineImpactMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
