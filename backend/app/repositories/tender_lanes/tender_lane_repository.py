
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_lane import TenderLane


class TenderLaneRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_all(self) -> list[TenderLane]:
        result = await self._session.scalars(
            select(TenderLane).order_by(TenderLane.created_at.desc(), TenderLane.id),
        )
        return list(result.all())

    async def add(self, row: TenderLane) -> TenderLane:
        self._session.add(row)
        await self._session.flush()
        return row
