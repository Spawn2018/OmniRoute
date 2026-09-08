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

    async def add(self, row: Tender) -> Tender:
        self._session.add(row)
        await self._session.flush()
        return row
