from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sales_invoice import SalesInvoice


class SalesInvoiceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[SalesInvoice]:
        result = await self._session.scalars(
            select(SalesInvoice).order_by(SalesInvoice.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: SalesInvoice) -> SalesInvoice:
        self._session.add(row)
        await self._session.flush()
        return row

    async def get(self, invoice_id: UUID) -> SalesInvoice | None:
        return await self._session.get(SalesInvoice, invoice_id)
