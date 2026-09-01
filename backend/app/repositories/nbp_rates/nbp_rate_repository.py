from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.nbp_rate import NbpRate


class NbpRateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[NbpRate]:
        result = await self._session.scalars(
            select(NbpRate).order_by(NbpRate.currency, NbpRate.rate_date.desc()),
        )
        return list(result.all())

    async def find_as_of(self, currency: str, on_date: date) -> NbpRate | None:
        stmt = (
            select(NbpRate)
            .where(NbpRate.currency == currency, NbpRate.rate_date <= on_date)
            .order_by(NbpRate.rate_date.desc())
            .limit(1)
        )
        found = await self._session.scalar(stmt)
        return found if isinstance(found, NbpRate) else None

    async def add(self, row: NbpRate) -> NbpRate:
        self._session.add(row)
        await self._session.flush()
        return row
