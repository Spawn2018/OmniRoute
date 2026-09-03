from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.collective_invoice import (
    require_collective_invoice_id,
    require_collective_shipment_id,
    require_collective_source_ref,
)
from app.domain.errors import InvalidCollectiveInvoice
from app.models.collective_invoice import CollectiveInvoice
from app.repositories.collective_invoices.collective_invoice_repository import (
    CollectiveInvoiceRepository,
)


class CollectiveInvoiceService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CollectiveInvoiceRepository(session)

    async def list_members(self) -> list[CollectiveInvoice]:
        return await self._rows.list_all()

    async def record_member(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        sales_invoice_id: UUID,
        shipment_id: UUID,
        source_ref: str,
    ) -> CollectiveInvoice:
        row = CollectiveInvoice(
            id=uuid4(),
            organization_id=organization_id,
            sales_invoice_id=require_collective_invoice_id(sales_invoice_id),
            shipment_id=require_collective_shipment_id(shipment_id),
            source_ref=require_collective_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidCollectiveInvoice("para już zapisana") from orig
