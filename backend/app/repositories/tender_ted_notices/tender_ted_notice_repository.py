from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_ted_notice import TenderTedNotice


class TenderTedNoticeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_notices(self) -> list[TenderTedNotice]:
        packed = await self._session.scalars(
            select(TenderTedNotice).order_by(
                TenderTedNotice.created_at.desc(),
                TenderTedNotice.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: TenderTedNotice) -> TenderTedNotice:
        self._session.add(row)
        await self._session.flush()
        return row
