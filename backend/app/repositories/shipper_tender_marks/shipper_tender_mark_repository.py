from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipper_tender_mark import ShipperTenderMark


class ShipperTenderMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ShipperTenderMark]:
        packed = await self._session.scalars(
            select(ShipperTenderMark).order_by(
                ShipperTenderMark.mark_code,
                ShipperTenderMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: ShipperTenderMark) -> ShipperTenderMark:
        self._session.add(row)
        await self._session.flush()
        return row
