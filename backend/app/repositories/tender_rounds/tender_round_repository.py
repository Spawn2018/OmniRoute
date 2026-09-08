from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_round import TenderRound


class TenderRoundRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[TenderRound]:
        result = await self._session.scalars(
            select(TenderRound).order_by(TenderRound.created_at.desc(), TenderRound.id),
        )
        return list(result.all())

    async def add(self, row: TenderRound) -> TenderRound:
        self._session.add(row)
        await self._session.flush()
        return row
