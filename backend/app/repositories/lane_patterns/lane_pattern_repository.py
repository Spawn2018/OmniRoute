from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lane_pattern import LanePattern


class LanePatternRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_patterns(self) -> list[LanePattern]:
        packed = await self._session.scalars(
            select(LanePattern).order_by(
                LanePattern.created_at.desc(),
                LanePattern.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: LanePattern) -> LanePattern:
        self._session.add(row)
        await self._session.flush()
        return row
