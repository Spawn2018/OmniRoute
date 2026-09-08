
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipment_package import ShipmentPackage


class ShipmentPackageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[ShipmentPackage]:
        result = await self._session.scalars(
            select(ShipmentPackage).order_by(ShipmentPackage.created_at.desc(), ShipmentPackage.id),
        )
        return list(result.all())

    async def add(self, row: ShipmentPackage) -> ShipmentPackage:
        self._session.add(row)
        await self._session.flush()
        return row
