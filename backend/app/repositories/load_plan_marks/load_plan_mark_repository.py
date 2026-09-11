from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.load_plan_mark import LoadPlanMark


class LoadPlanMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[LoadPlanMark]:
        packed = await self._session.scalars(
            select(LoadPlanMark).order_by(LoadPlanMark.mark_code, LoadPlanMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: LoadPlanMark) -> LoadPlanMark:
        self._session.add(row)
        await self._session.flush()
        return row
