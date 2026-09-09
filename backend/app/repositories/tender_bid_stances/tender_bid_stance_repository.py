from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_bid_stance import TenderBidStance


class TenderBidStanceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_stances(self) -> list[TenderBidStance]:
        result = await self._session.scalars(
            select(TenderBidStance).order_by(
                TenderBidStance.created_at.desc(),
                TenderBidStance.id,
            ),
        )
        return list(result.all())

    async def add(self, row: TenderBidStance) -> TenderBidStance:
        self._session.add(row)
        await self._session.flush()
        return row
