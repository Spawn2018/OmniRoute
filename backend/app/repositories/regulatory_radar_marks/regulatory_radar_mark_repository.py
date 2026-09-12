from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.regulatory_radar_mark import RegulatoryRadarMark


class RegulatoryRadarMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RegulatoryRadarMark]:
        packed = await self._session.scalars(
            select(RegulatoryRadarMark).order_by(
                RegulatoryRadarMark.mark_code,
                RegulatoryRadarMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: RegulatoryRadarMark) -> RegulatoryRadarMark:
        self._session.add(row)
        await self._session.flush()
        return row
