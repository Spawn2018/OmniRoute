from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_win_loss import TenderWinLoss


class TenderWinLossRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_verdicts(self) -> list[TenderWinLoss]:
        result = await self._session.scalars(
            select(TenderWinLoss).order_by(
                TenderWinLoss.created_at.desc(),
                TenderWinLoss.id,
            ),
        )
        return list(result.all())

    async def add(self, row: TenderWinLoss) -> TenderWinLoss:
        self._session.add(row)
        await self._session.flush()
        return row
