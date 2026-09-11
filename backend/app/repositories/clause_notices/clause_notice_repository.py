from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.clause_notice import ClauseNotice


class ClauseNoticeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_notices(self) -> list[ClauseNotice]:
        packed = await self._session.scalars(
            select(ClauseNotice).order_by(
                ClauseNotice.notice_code,
                ClauseNotice.id,
            ),
        )
        return list(packed.all())

    async def add_notice(self, row: ClauseNotice) -> ClauseNotice:
        self._session.add(row)
        await self._session.flush()
        return row
