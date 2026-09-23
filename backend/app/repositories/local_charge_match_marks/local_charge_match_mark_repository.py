from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.local_charge_match_mark import LocalChargeMatchMark


class LocalChargeMatchMarkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_marks(self) -> list[LocalChargeMatchMark]:
        result = await self._db.scalars(
            select(LocalChargeMatchMark).order_by(
                LocalChargeMatchMark.match_kind.asc(),
                LocalChargeMatchMark.mark_code.asc(),
                LocalChargeMatchMark.id.asc(),
            ),
        )
        return list(result.all())

    async def add_mark(self, row: LocalChargeMatchMark) -> LocalChargeMatchMark:
        self._db.add(row)
        await self._db.flush()
        return row
