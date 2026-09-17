from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice_alloc_mark import InvoiceAllocMark


class InvoiceAllocMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[InvoiceAllocMark]:
        packed = await self._session.scalars(
            select(InvoiceAllocMark).order_by(
                InvoiceAllocMark.mark_code,
                InvoiceAllocMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: InvoiceAllocMark) -> InvoiceAllocMark:
        self._session.add(row)
        await self._session.flush()
        return row
