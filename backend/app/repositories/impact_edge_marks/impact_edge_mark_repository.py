from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.impact_edge_mark import ImpactEdgeMark


class ImpactEdgeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ImpactEdgeMark]:
        packed = await self._session.scalars(
            select(ImpactEdgeMark).order_by(
                ImpactEdgeMark.mark_code,
                ImpactEdgeMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: ImpactEdgeMark) -> ImpactEdgeMark:
        self._session.add(row)
        await self._session.flush()
        return row
