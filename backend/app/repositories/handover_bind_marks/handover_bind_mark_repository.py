from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.handover_bind_mark import HandoverBindMark


class HandoverBindMarkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_marks(self) -> list[HandoverBindMark]:
        result = await self._db.scalars(
            select(HandoverBindMark).order_by(
                HandoverBindMark.bind_kind.asc(),
                HandoverBindMark.mark_code.asc(),
                HandoverBindMark.id.asc(),
            ),
        )
        return list(result.all())

    async def add_mark(self, row: HandoverBindMark) -> HandoverBindMark:
        self._db.add(row)
        await self._db.flush()
        return row
