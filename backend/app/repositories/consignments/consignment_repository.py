from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consignment import Consignment


class ConsignmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Consignment]:
        result = await self._session.scalars(
            select(Consignment).order_by(
                Consignment.created_at.desc(),
                Consignment.id,
            ),
        )
        return list(result.all())

    async def get_by_id(self, consignment_id: object) -> Consignment | None:
        loaded = await self._session.scalar(
            select(Consignment).where(Consignment.id == consignment_id).limit(1),
        )
        if loaded is None:
            return None
        return loaded

    async def count_for_shipment(self, shipment_id: object) -> int:
        total = await self._session.scalar(
            select(func.count())
            .select_from(Consignment)
            .where(Consignment.shipment_id == shipment_id),
        )
        return int(total or 0)

    async def add(self, row: Consignment) -> Consignment:
        self._session.add(row)
        await self._session.flush()
        return row
