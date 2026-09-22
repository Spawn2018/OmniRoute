from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.clone_carry_mark import CloneCarryMark


class CloneCarryMarkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_marks(self) -> list[CloneCarryMark]:
        result = await self._db.scalars(
            select(CloneCarryMark).order_by(
                CloneCarryMark.carry_kind.asc(),
                CloneCarryMark.mark_code.asc(),
                CloneCarryMark.id.asc(),
            ),
        )
        return list(result.all())

    async def add_mark(self, row: CloneCarryMark) -> CloneCarryMark:
        self._db.add(row)
        await self._db.flush()
        return row
