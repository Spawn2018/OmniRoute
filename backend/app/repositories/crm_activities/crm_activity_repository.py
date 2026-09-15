from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.crm_activity import CrmActivity


class CrmActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_activities(self) -> list[CrmActivity]:
        packed = await self._session.scalars(
            select(CrmActivity).order_by(
                CrmActivity.activity_code,
                CrmActivity.id,
            ),
        )
        return list(packed.all())

    async def add_activity(self, row: CrmActivity) -> CrmActivity:
        self._session.add(row)
        await self._session.flush()
        return row
