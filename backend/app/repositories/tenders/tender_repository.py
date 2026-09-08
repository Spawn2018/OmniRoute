from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender import Tender


class TenderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Tender]:
        result = await self._session.scalars(
            select(Tender).order_by(Tender.created_at.desc(), Tender.id),
        )
        return list(result.all())

    async def get(self, tender_id: UUID) -> Tender | None:
        return await self._session.get(Tender, tender_id)

    async def add(self, row: Tender) -> Tender:
        self._session.add(row)
        await self._session.flush()
        return row
