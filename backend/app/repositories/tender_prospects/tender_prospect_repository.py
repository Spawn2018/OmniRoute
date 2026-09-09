from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_prospect import TenderProspect


class TenderProspectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_prospects(self) -> list[TenderProspect]:
        result = await self._session.scalars(
            select(TenderProspect).order_by(
                TenderProspect.created_at.desc(),
                TenderProspect.id,
            ),
        )
        return list(result.all())

    async def add(self, row: TenderProspect) -> TenderProspect:
        self._session.add(row)
        await self._session.flush()
        return row
