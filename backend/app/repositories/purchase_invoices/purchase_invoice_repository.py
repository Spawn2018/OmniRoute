from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.purchase_invoice import PurchaseInvoice


class PurchaseInvoiceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_invoices(self) -> list[PurchaseInvoice]:
        packed = await self._session.scalars(
            select(PurchaseInvoice).order_by(
                PurchaseInvoice.invoice_ref,
                PurchaseInvoice.id,
            ),
        )
        return list(packed.all())

    async def add_invoice(self, row: PurchaseInvoice) -> PurchaseInvoice:
        self._session.add(row)
        await self._session.flush()
        return row
