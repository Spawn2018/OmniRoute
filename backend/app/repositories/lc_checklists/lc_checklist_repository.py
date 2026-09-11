from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lc_checklist import LcChecklist


class LcChecklistRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_checklists(self) -> list[LcChecklist]:
        packed = await self._session.scalars(
            select(LcChecklist).order_by(LcChecklist.checklist_code, LcChecklist.id),
        )
        return list(packed.all())

    async def add_checklist(self, row: LcChecklist) -> LcChecklist:
        self._session.add(row)
        await self._session.flush()
        return row
