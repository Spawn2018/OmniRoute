from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.sales_invoice import (
    require_invoice_kind,
    require_invoice_ref,
    require_invoice_shipment_id,
    require_invoice_source_ref,
)
from app.models.sales_invoice import SalesInvoice
from app.repositories.sales_invoices.sales_invoice_repository import SalesInvoiceRepository


class SalesInvoiceService:
    def __init__(self, session: AsyncSession) -> None:
        self._invoices = SalesInvoiceRepository(session)

    async def list_invoices(self) -> list[SalesInvoice]:
        return await self._invoices.list_all()

    async def record_invoice(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        invoice_kind: str,
        invoice_ref: str,
        source_ref: str,
    ) -> SalesInvoice:
        row = SalesInvoice(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_invoice_shipment_id(shipment_id),
            invoice_kind=require_invoice_kind(invoice_kind),
            invoice_ref=require_invoice_ref(invoice_ref),
            source_ref=require_invoice_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._invoices.add(row)
