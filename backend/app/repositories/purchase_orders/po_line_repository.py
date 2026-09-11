from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.po_line import PoLine
from app.models.purchase_order import PurchaseOrder


class PoLineRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_lines(self) -> list[PoLine]:
        packed = await self._session.scalars(
            select(PoLine).order_by(PoLine.line_code, PoLine.id),
        )
        return list(packed.all())

    async def get_header(self, purchase_order_id: UUID) -> PurchaseOrder | None:
        packed = await self._session.scalars(
            select(PurchaseOrder).where(PurchaseOrder.id == purchase_order_id)
        )
        return packed.first()

    async def add_line(self, row: PoLine) -> PoLine:
        self._session.add(row)
        await self._session.flush()
        return row
