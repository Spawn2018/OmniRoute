from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_quote import TenderQuote


class TenderQuoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[TenderQuote]:
        result = await self._session.scalars(
            select(TenderQuote).order_by(TenderQuote.created_at.desc(), TenderQuote.id),
        )
        return list(result.all())

    async def add(self, row: TenderQuote) -> TenderQuote:
        self._session.add(row)
        await self._session.flush()
        return row
