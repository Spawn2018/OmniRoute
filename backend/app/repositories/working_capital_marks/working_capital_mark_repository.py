from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.working_capital_mark import WorkingCapitalMark


class WorkingCapitalMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[WorkingCapitalMark]:
        packed = await self._session.scalars(
            select(WorkingCapitalMark).order_by(
                WorkingCapitalMark.mark_code,
                WorkingCapitalMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: WorkingCapitalMark) -> WorkingCapitalMark:
        self._session.add(row)
        await self._session.flush()
        return row
