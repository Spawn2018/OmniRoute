from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_carbon_mark import TenderCarbonMark


class TenderCarbonMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_marks(self) -> list[TenderCarbonMark]:
        packed = await self._session.scalars(
            select(TenderCarbonMark).order_by(
                TenderCarbonMark.created_at.desc(),
                TenderCarbonMark.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: TenderCarbonMark) -> TenderCarbonMark:
        self._session.add(row)
        await self._session.flush()
        return row
