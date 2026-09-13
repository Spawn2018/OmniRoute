from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sales_lane import SalesLane


class SalesLaneRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_lanes(self) -> list[SalesLane]:
        packed = await self._session.scalars(
            select(SalesLane).order_by(
                SalesLane.lane_code,
                SalesLane.id,
            ),
        )
        return list(packed.all())

    async def add_lane(self, row: SalesLane) -> SalesLane:
        self._session.add(row)
        await self._session.flush()
        return row
