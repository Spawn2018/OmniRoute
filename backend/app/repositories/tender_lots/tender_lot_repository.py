from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_lot import TenderLot


class TenderLotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[TenderLot]:
        result = await self._session.scalars(
            select(TenderLot).order_by(TenderLot.created_at.desc(), TenderLot.id),
        )
        return list(result.all())

    async def get(self, lot_id: UUID) -> TenderLot | None:
        return await self._session.get(TenderLot, lot_id)

    async def add(self, row: TenderLot) -> TenderLot:
        self._session.add(row)
        await self._session.flush()
        return row
