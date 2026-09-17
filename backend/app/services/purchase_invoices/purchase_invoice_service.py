from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.purchase_invoice import parse_purchase_invoice_row
from app.models.purchase_invoice import PurchaseInvoice
from app.repositories.purchase_invoices.purchase_invoice_repository import (
    PurchaseInvoiceRepository,
)


class PurchaseInvoiceService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PurchaseInvoiceRepository(session)

    async def list_invoices(self) -> list[PurchaseInvoice]:
        return await self._rows.list_invoices()

    async def persist_purchase_invoice(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        invoice_ref: object,
        invoice_kind: object,
        source_ref: object,
    ) -> PurchaseInvoice:
        ref, kind, origin = parse_purchase_invoice_row(
            invoice_ref,
            invoice_kind,
            source_ref,
        )
        row = PurchaseInvoice(
            id=uuid4(),
            organization_id=organization_id,
            invoice_ref=ref,
            invoice_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_invoice(row)
