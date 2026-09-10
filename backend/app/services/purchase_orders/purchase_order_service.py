from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.purchase_order import parse_purchase_order_row
from app.models.purchase_order import PurchaseOrder
from app.repositories.purchase_orders.purchase_order_repository import PurchaseOrderRepository


class PurchaseOrderService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PurchaseOrderRepository(session)

    async def list_headers(self) -> list[PurchaseOrder]:
        return await self._rows.list_headers()

    async def persist_purchase_order(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        po_code: object,
        plant_label: object,
        source_ref: object,
    ) -> PurchaseOrder:
        code, plant, origin = parse_purchase_order_row(po_code, plant_label, source_ref)
        row = PurchaseOrder(
            id=uuid4(),
            organization_id=organization_id,
            po_code=code,
            plant_label=plant,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_header(row)
