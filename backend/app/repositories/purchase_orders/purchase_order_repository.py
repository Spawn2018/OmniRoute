from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.purchase_order import PurchaseOrder


class PurchaseOrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_headers(self) -> list[PurchaseOrder]:
        packed = await self._session.scalars(
            select(PurchaseOrder).order_by(PurchaseOrder.po_code, PurchaseOrder.id),
        )
        return list(packed.all())

    async def add_header(self, row: PurchaseOrder) -> PurchaseOrder:
        self._session.add(row)
        await self._session.flush()
        return row
