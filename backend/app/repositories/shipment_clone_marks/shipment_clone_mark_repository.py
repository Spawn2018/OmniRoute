from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipment_clone_mark import ShipmentCloneMark


class ShipmentCloneMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ShipmentCloneMark]:
        stmt = select(ShipmentCloneMark).order_by(
            ShipmentCloneMark.mark_code,
            ShipmentCloneMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: ShipmentCloneMark) -> ShipmentCloneMark:
        self._session.add(row)
        await self._session.flush()
        return row
