from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.crm_dedup_mark import CrmDedupMark


class CrmDedupMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CrmDedupMark]:
        packed = await self._session.scalars(
            select(CrmDedupMark).order_by(
                CrmDedupMark.mark_code,
                CrmDedupMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CrmDedupMark) -> CrmDedupMark:
        self._session.add(row)
        await self._session.flush()
        return row
