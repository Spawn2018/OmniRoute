from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.executive_mark import ExecutiveMark


class ExecutiveMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    async def fetch_briefs(self) -> list[ExecutiveMark]:
        stmt = select(ExecutiveMark).order_by(ExecutiveMark.question_kind, ExecutiveMark.id)
        executed = await self._db.execute(stmt)
        return list(executed.scalars())

    async def add(self, row: ExecutiveMark) -> ExecutiveMark:
        self._db.add(row)
        await self._db.flush()
        return row
