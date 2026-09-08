from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipment_stakeholder import ShipmentStakeholder


class ShipmentStakeholderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_current_for_shipment(
        self,
        shipment_id: UUID,
    ) -> list[ShipmentStakeholder]:
        result = await self._session.scalars(
            select(ShipmentStakeholder)
            .where(
                ShipmentStakeholder.shipment_id == shipment_id,
                ShipmentStakeholder.superseded_by.is_(None),
            )
            .order_by(ShipmentStakeholder.role, ShipmentStakeholder.id),
        )
        return list(result.all())

    async def find_current(
        self,
        shipment_id: UUID,
        role: str,
    ) -> ShipmentStakeholder | None:
        result = await self._session.scalars(
            select(ShipmentStakeholder).where(
                ShipmentStakeholder.shipment_id == shipment_id,
                ShipmentStakeholder.role == role,
                ShipmentStakeholder.superseded_by.is_(None),
            ),
        )
        found = list(result.all())
        return found[0] if found else None

    async def add(self, row: ShipmentStakeholder) -> ShipmentStakeholder:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(
        self,
        current: ShipmentStakeholder,
        successor_id: UUID,
    ) -> ShipmentStakeholder:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
