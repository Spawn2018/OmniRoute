from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lane_km import LaneKm


class LaneKmRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[LaneKm]:
        packed = await self._session.scalars(
            select(LaneKm).order_by(
                LaneKm.km_code,
                LaneKm.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: LaneKm) -> LaneKm:
        self._session.add(row)
        await self._session.flush()
        return row
