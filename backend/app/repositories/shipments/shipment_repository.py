
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipment import Shipment


class ShipmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Shipment]:
        result = await self._session.scalars(
            select(Shipment).order_by(Shipment.created_at.desc()),
        )
        return list(result.all())

    async def get(self, shipment_id: UUID) -> Shipment | None:
        found = await self._session.get(Shipment, shipment_id)
        return found if isinstance(found, Shipment) else None

    async def add(self, row: Shipment) -> Shipment:
        self._session.add(row)
        await self._session.flush()
        return row
