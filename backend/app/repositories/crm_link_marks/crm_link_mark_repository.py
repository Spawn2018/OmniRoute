from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.crm_link_mark import CrmLinkMark


class CrmLinkMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CrmLinkMark]:
        packed = await self._session.scalars(
            select(CrmLinkMark).order_by(
                CrmLinkMark.mark_code,
                CrmLinkMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CrmLinkMark) -> CrmLinkMark:
        self._session.add(row)
        await self._session.flush()
        return row
