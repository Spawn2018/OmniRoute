from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asn import Asn
from app.models.purchase_order import PurchaseOrder


class AsnRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_notices(self) -> list[Asn]:
        packed = await self._session.scalars(
            select(Asn).order_by(Asn.asn_code, Asn.id),
        )
        return list(packed.all())

    async def get_header(self, purchase_order_id: UUID) -> PurchaseOrder | None:
        packed = await self._session.scalars(
            select(PurchaseOrder).where(PurchaseOrder.id == purchase_order_id)
        )
        return packed.first()

    async def add_notice(self, row: Asn) -> Asn:
        self._session.add(row)
        await self._session.flush()
        return row
