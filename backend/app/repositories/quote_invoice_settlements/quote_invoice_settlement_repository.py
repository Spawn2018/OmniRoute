from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quote_invoice_settlement import QuoteInvoiceSettlement


class QuoteInvoiceSettlementRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[QuoteInvoiceSettlement]:
        result = await self._session.scalars(
            select(QuoteInvoiceSettlement).order_by(QuoteInvoiceSettlement.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: QuoteInvoiceSettlement) -> QuoteInvoiceSettlement:
        self._session.add(row)
        await self._session.flush()
        return row
