from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.collective_invoice import CollectiveInvoice


class CollectiveInvoiceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[CollectiveInvoice]:
        result = await self._session.scalars(
            select(CollectiveInvoice).order_by(CollectiveInvoice.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: CollectiveInvoice) -> CollectiveInvoice:
        self._session.add(row)
        await self._session.flush()
        return row
