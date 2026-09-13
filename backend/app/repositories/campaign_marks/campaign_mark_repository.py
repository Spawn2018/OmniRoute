from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign_mark import CampaignMark


class CampaignMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CampaignMark]:
        packed = await self._session.scalars(
            select(CampaignMark).order_by(
                CampaignMark.mark_code,
                CampaignMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CampaignMark) -> CampaignMark:
        self._session.add(row)
        await self._session.flush()
        return row
