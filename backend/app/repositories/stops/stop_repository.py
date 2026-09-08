from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stop import Stop


class StopRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_current_for_shipment(self, shipment_id: UUID) -> list[Stop]:
        result = await self._session.scalars(
            select(Stop)
            .where(Stop.shipment_id == shipment_id, Stop.superseded_by.is_(None))
            .order_by(Stop.sequence_no, Stop.id),
        )
        return list(result.all())

    async def find_current(self, shipment_id: UUID, sequence_no: int) -> Stop | None:
        result = await self._session.scalars(
            select(Stop).where(
                Stop.shipment_id == shipment_id,
                Stop.sequence_no == sequence_no,
                Stop.superseded_by.is_(None),
            ),
        )
        found = list(result.all())
        return found[0] if found else None

    async def add(self, row: Stop) -> Stop:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(self, current: Stop, successor_id: UUID) -> Stop:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
