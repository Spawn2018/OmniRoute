from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_playbook import TenderPlaybook


class TenderPlaybookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_plays(self) -> list[TenderPlaybook]:
        result = await self._session.scalars(
            select(TenderPlaybook).order_by(
                TenderPlaybook.created_at.desc(),
                TenderPlaybook.id,
            ),
        )
        return list(result.all())

    async def add(self, row: TenderPlaybook) -> TenderPlaybook:
        self._session.add(row)
        await self._session.flush()
        return row
