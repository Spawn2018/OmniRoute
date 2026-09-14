from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.line_impact_layer_mark import LineImpactLayerMark


class LineImpactLayerMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[LineImpactLayerMark]:
        stmt = select(LineImpactLayerMark).order_by(
            LineImpactLayerMark.mark_code,
            LineImpactLayerMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: LineImpactLayerMark) -> LineImpactLayerMark:
        self._session.add(row)
        await self._session.flush()
        return row
