from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipment_leg import ShipmentLeg


class ShipmentLegRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[ShipmentLeg]:
        result = await self._session.scalars(
            select(ShipmentLeg).order_by(ShipmentLeg.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: ShipmentLeg) -> ShipmentLeg:
        self._session.add(row)
        await self._session.flush()
        return row
